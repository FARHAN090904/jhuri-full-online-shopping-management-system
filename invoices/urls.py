from django.urls import path
from .views import UploadInvoicePDFView, DownloadInvoicePDFView, MyInvoicesView

urlpatterns = [
    path('upload-pdf/', UploadInvoicePDFView.as_view(), name='upload-invoice-pdf'),
    path('my-invoices/', MyInvoicesView.as_view(), name='my-invoices'),
    path('<int:order_id>/download-pdf/', DownloadInvoicePDFView.as_view(), name='download-invoice-pdf'),
]