import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts.authentication import UserAuthentication
from orders.models import Order
from .models import Payment


class PaymentCallbackView(APIView):
    """
    Called by the frontend after order is placed to record payment.
    For Cash on Delivery: marks as pending.
    For others: marks as completed (integrate real payment gateway here).
    """
    authentication_classes = [UserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        method = request.data.get('method', 'cash_on_delivery')
        transaction_ref = request.data.get('transaction_ref', '')

        try:
            order = Order.objects.get(order_id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=404)

        # Don't create duplicate payments
        if Payment.objects.filter(order=order).exists():
            payment = Payment.objects.get(order=order)
            return Response({
                'payment_id': payment.payment_id,
                'status': payment.status,
                'message': 'Payment already recorded.'
            })

        # COD stays pending; other methods auto-complete (demo)
        status = 'pending' if method == 'cash_on_delivery' else 'completed'
        paid_at = None if method == 'cash_on_delivery' else datetime.datetime.now()

        payment = Payment.objects.create(
            order=order,
            method=method,
            status=status,
            amount=order.total_amount,
            transaction_ref=transaction_ref or None,
            paid_at=paid_at,
        )

        # If paid, confirm order
        if status == 'completed':
            Order.objects.filter(order_id=order_id).update(status='confirmed')

        return Response({
            'payment_id': payment.payment_id,
            'status': payment.status,
            'amount': str(payment.amount),
            'message': 'Payment recorded successfully.',
        }, status=201)
