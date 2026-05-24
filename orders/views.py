import base64
import datetime
from decimal import Decimal

from django.utils import timezone
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.authentication import UserAuthentication
from accounts.models import Address
from cart.models import Cart, CartItem
from products.models import Product
from .models import Order, OrderItem, Invoice, Coupon, InvoicePdf
from .utils import generate_invoice_pdf

SHIPPING_FEE = Decimal('60.00')


def _get_user(request):
    auth = UserAuthentication()
    try:
        user, _ = auth.authenticate(request)
        return user
    except Exception:
        return None


def _calculate_discount(coupon, subtotal):
    if coupon.discount_type == 'percentage':
        return (subtotal * coupon.discount_value / 100).quantize(Decimal('0.01'))
    return min(coupon.discount_value, subtotal)


class CheckoutView(APIView):
    authentication_classes = []
    permission_classes = []

    @transaction.atomic
    def post(self, request):
        user = _get_user(request)
        if not user:
            return Response({'error': 'Authentication required.'}, status=401)

        address_id = request.data.get('address_id')
        coupon_code = request.data.get('coupon_code', '').strip().upper()
        notes = request.data.get('notes', '')

        try:
            address = Address.objects.get(address_id=address_id, user=user)
        except Address.DoesNotExist:
            return Response({'error': 'Invalid address.'}, status=400)

        try:
            cart = Cart.objects.prefetch_related('items__product').get(user=user)
        except Cart.DoesNotExist:
            return Response({'error': 'Your cart is empty.'}, status=400)

        cart_items = list(cart.items.select_related('product').all())
        if not cart_items:
            return Response({'error': 'Your cart is empty.'}, status=400)

        for item in cart_items:
            if item.product.stock_qty < item.quantity:
                return Response(
                    {'error': f'Insufficient stock for {item.product.product_name}.'},
                    status=400
                )

        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        shipping_fee = SHIPPING_FEE
        discount_amount = Decimal('0')
        coupon = None

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                discount_amount = _calculate_discount(coupon, subtotal)
            except Coupon.DoesNotExist:
                return Response({'error': 'Invalid coupon code.'}, status=400)

        total_amount = subtotal - discount_amount + shipping_fee

        # Step 1: Create order
        order = Order.objects.create(
            user=user,
            address=address,
            subtotal=subtotal,
            discount_amount=discount_amount,
            shipping_fee=shipping_fee,
            total_amount=total_amount,
            notes=notes,
            status='pending',
        )

        # Step 2: Create order items & update stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.price,
                total_price=item.product.price * item.quantity,
            )
            Product.objects.filter(pk=item.product.product_id).update(
                stock_qty=item.product.stock_qty - item.quantity
            )

        if coupon:
            Coupon.objects.filter(pk=coupon.pk).update(
                used_count=coupon.used_count + 1
            )

        # Step 3: Create invoice
        invoice_number = f"INV-{timezone.now().year}-{order.order_id:05d}"
        invoice = Invoice.objects.create(
            order=order,
            invoice_number=invoice_number,
            total_amount=total_amount,
            status='issued',
        )

        # Step 4: Generate PDF & save to invoice_pdfs
        pdf_error = None
        try:
            order_items = OrderItem.objects.filter(order=order).select_related('product')
            pdf_bytes = generate_invoice_pdf(
                order=order,
                invoice=invoice,
                user=user,
                address=address,
                items=order_items,
            )
            pdf_base64_str = base64.b64encode(pdf_bytes).decode('utf-8')
            file_size_kb = round(len(pdf_bytes) / 1024, 2)

            InvoicePdf.objects.create(
                invoice=invoice,
                order=order,
                user=user,
                filename=f"invoice_{invoice_number}.pdf",
                pdf_base64=pdf_base64_str,
                file_size_kb=file_size_kb,
            )
        except Exception as e:
            pdf_error = str(e)

        # Step 5: Clear cart
        cart.items.all().delete()

        response_data = {
            'order_id': order.order_id,
            'invoice_number': invoice_number,
            'invoice_id': invoice.invoice_id,
        }
        if pdf_error:
            response_data['pdf_warning'] = f'PDF saved but DB error: {pdf_error}'

        return Response(response_data, status=201)


class OrderDetailView(APIView):
    authentication_classes = [UserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.select_related('address').get(
                order_id=order_id,
                user=request.user
            )
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=404)

        items = OrderItem.objects.filter(order=order).select_related('product')

        return Response({
            'order_id': order.order_id,
            'status': order.status,
            'ordered_at': str(order.ordered_at),
            'subtotal': str(order.subtotal),
            'discount_amount': str(order.discount_amount),
            'shipping_fee': str(order.shipping_fee),
            'total_amount': str(order.total_amount),
            'address': {
                'street': order.address.street,
                'city': order.address.city,
                'state': order.address.state,
                'postal_code': order.address.postal_code,
                'country': order.address.country,
            },
            'items': [
                {
                    'order_item_id': item.order_item_id,
                    'product_id': item.product_id,
                    'product_name': item.product.product_name,
                    'quantity': item.quantity,
                    'unit_price': str(item.unit_price),
                    'total_price': str(item.total_price),
                }
                for item in items
            ]
        })


class OrderListView(APIView):
    authentication_classes = [UserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
        return Response([
            {
                'order_id': o.order_id,
                'status': o.status,
                'total_amount': str(o.total_amount),
                'ordered_at': str(o.ordered_at),
            }
            for o in orders
        ])
from django.http import HttpResponse

class InvoiceDownloadView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=404)

        try:
            invoice_pdf = InvoicePdf.objects.get(order=order)
        except InvoicePdf.DoesNotExist:
            return Response({'error': 'Invoice PDF not found.'}, status=404)

        pdf_bytes = base64.b64decode(invoice_pdf.pdf_base64)

        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{invoice_pdf.filename}"'
        return response