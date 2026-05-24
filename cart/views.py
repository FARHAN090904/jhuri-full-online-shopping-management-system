from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.authentication import UserAuthentication
from products.models import Product
from .models import Cart, CartItem

SHIPPING_FEE = Decimal('60.00')


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def build_cart_response(cart):
    items = CartItem.objects.filter(cart=cart).select_related('product__category')
    subtotal = Decimal('0')
    item_data = []

    for item in items:
        line_total = item.product.price * item.quantity
        subtotal += line_total
        item_data.append({
            'cart_item_id': item.cart_item_id,
            'product_id': item.product.product_id,
            'product_name': item.product.product_name,
            'category_name': item.product.category.category_name if item.product.category else '',
            'price': str(item.product.price),
            'quantity': item.quantity,
            'line_total': str(line_total),
            'stock_qty': item.product.stock_qty,
            'image_url': item.product.image_url,
        })

    shipping = SHIPPING_FEE if item_data else Decimal('0')
    total = subtotal + shipping

    return {
        'cart_id': cart.cart_id,
        'items': item_data,
        'subtotal': str(subtotal),
        'shipping_fee': str(shipping),
        'total': str(total),
        'item_count': len(item_data),
    }


class CartView(APIView):
    authentication_classes = [UserAuthentication]
    permission_classes = [IsAuthenticated]

    # GET /api/cart/  — return user's cart
    def get(self, request):
        cart = get_or_create_cart(request.user)
        return Response(build_cart_response(cart))

    # POST /api/cart/  — add item
    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=404)

        if product.stock_qty < 1:
            return Response({'error': 'Product is out of stock.'}, status=400)

        cart = get_or_create_cart(request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            new_qty = item.quantity + quantity
            if new_qty > product.stock_qty:
                return Response({'error': f'Only {product.stock_qty} in stock.'}, status=400)
            item.quantity = new_qty
            item.save()

        return Response(build_cart_response(cart), status=201)

    # PUT /api/cart/  — update quantity
    def put(self, request):
        cart_item_id = request.data.get('cart_item_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            item = CartItem.objects.select_related('product', 'cart').get(
                cart_item_id=cart_item_id,
                cart__user=request.user
            )
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found.'}, status=404)

        if quantity < 1:
            return Response({'error': 'Quantity must be at least 1.'}, status=400)

        if quantity > item.product.stock_qty:
            return Response({'error': f'Only {item.product.stock_qty} in stock.'}, status=400)

        item.quantity = quantity
        item.save()

        return Response(build_cart_response(item.cart))

    # DELETE /api/cart/  — remove item
    def delete(self, request):
        cart_item_id = request.data.get('cart_item_id')

        try:
            item = CartItem.objects.get(
                cart_item_id=cart_item_id,
                cart__user=request.user
            )
            cart = item.cart
            item.delete()
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found.'}, status=404)

        return Response(build_cart_response(cart))
