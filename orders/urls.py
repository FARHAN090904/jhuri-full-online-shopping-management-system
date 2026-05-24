from django.urls import path
from .views import CheckoutView, OrderDetailView, OrderListView, InvoiceDownloadView

urlpatterns = [
    path('checkout/', CheckoutView.as_view()),
    path('', OrderListView.as_view()),
    path('<int:order_id>/', OrderDetailView.as_view()),
    path('<int:order_id>/invoice/download/', InvoiceDownloadView.as_view()),
]