from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import base64


def _get_user(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth_header.startswith('Bearer '):
        return None
    token_str = auth_header.split(' ')[1]
    try:
        from rest_framework_simplejwt.tokens import AccessToken
        from accounts.models import User
        token = AccessToken(token_str)
        user_id = token.get('user_id')
        if not user_id:
            return None
        user = User.objects.select_related('role').get(pk=user_id, is_active=True)
        return user
    except Exception:
        return None


@method_decorator(csrf_exempt, name='dispatch')
class UploadInvoicePDFView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        user = _get_user(request)
        if not user:
            return Response({'error': 'Authentication required.'}, status=401)

        invoice_id = request.data.get('invoice_id')
        order_id   = request.data.get('order_id')
        pdf_base64 = request.data.get('pdf_base64', '')
        filename   = request.data.get('filename', f'invoice_{order_id}.pdf')

        if not invoice_id or not order_id or not pdf_base64:
            return Response({'error': 'invoice_id, order_id and pdf_base64 are required.'}, status=400)

        try:
            pdf_bytes    = base64.b64decode(pdf_base64)
            file_size_kb = round(len(pdf_bytes) / 1024, 2)
        except Exception:
            file_size_kb = None

        from .models import InvoicePDF
        obj, created = InvoicePDF.objects.update_or_create(
            invoice_id=invoice_id,
            defaults={
                'order_id'    : order_id,
                'user_id'     : user.user_id,
                'filename'    : filename,
                'pdf_base64'  : pdf_base64,
                'file_size_kb': file_size_kb,
            }
        )

        return Response({
            'message'     : 'PDF stored successfully.',
            'pdf_id'      : obj.pdf_id,
            'filename'    : obj.filename,
            'size_kb'     : float(obj.file_size_kb) if obj.file_size_kb else None,
        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class MyInvoicesView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        user = _get_user(request)
        if not user:
            return Response({'error': 'Authentication required.'}, status=401)

        from .models import InvoicePDF
        pdfs = InvoicePDF.objects.filter(user_id=user.user_id).order_by('-generated_at')
        return Response([
            {
                'pdf_id'      : p.pdf_id,
                'order_id'    : p.order_id,
                'invoice_id'  : p.invoice_id,
                'filename'    : p.filename,
                'file_size_kb': float(p.file_size_kb) if p.file_size_kb else None,
                'generated_at': p.generated_at,
                'has_pdf'     : bool(p.pdf_base64),
            }
            for p in pdfs
        ])


@method_decorator(csrf_exempt, name='dispatch')
class DownloadInvoicePDFView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, order_id):
        user = _get_user(request)
        if not user:
            return Response({'error': 'Authentication required.'}, status=401)

        from .models import InvoicePDF
        try:
            if user.role.role_name == 'admin':
                pdf = InvoicePDF.objects.get(order_id=order_id)
            else:
                pdf = InvoicePDF.objects.get(order_id=order_id, user_id=user.user_id)
        except InvoicePDF.DoesNotExist:
            return Response({'error': 'PDF not found.'}, status=404)

        try:
            pdf_bytes = base64.b64decode(pdf.pdf_base64)
        except Exception:
            return Response({'error': 'Invalid PDF data.'}, status=500)

        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf.filename}"'
        return response