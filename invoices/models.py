from django.db import models


class InvoicePDF(models.Model):
    pdf_id = models.AutoField(primary_key=True)
    invoice_id = models.IntegerField(unique=True)
    order_id = models.IntegerField()
    user_id = models.IntegerField()
    filename = models.CharField(max_length=200)
    pdf_base64 = models.TextField()
    file_size_kb = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'invoice_pdfs'

    def __str__(self):
        return self.filename