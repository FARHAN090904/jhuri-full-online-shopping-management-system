from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_invoice_pdf(order, invoice, user, address, items):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 60, f"Invoice: {invoice.invoice_number}")

    p.setFont("Helvetica", 12)
    p.drawString(50, height - 90,  f"Customer: {user.full_name}")
    p.drawString(50, height - 110, f"Mobile: {user.phone or 'N/A'}")
    p.drawString(50, height - 130, f"Address: {address.street}, {address.city}")
    p.drawString(50, height - 150, f"Order ID: {order.order_id}")
    p.drawString(50, height - 170, f"Total: Tk {order.total_amount}")

    y = height - 210
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50,  y, "Product")
    p.drawString(300, y, "Qty")
    p.drawString(380, y, "Unit Price")
    p.drawString(470, y, "Total")
    y -= 20

    p.setFont("Helvetica", 11)
    for item in items:
        p.drawString(50,  y, str(item.product.product_name)[:35])
        p.drawString(300, y, str(item.quantity))
        p.drawString(380, y, f"Tk {item.unit_price}")
        p.drawString(470, y, f"Tk {item.total_price}")
        y -= 20
        if y < 60:
            p.showPage()
            y = height - 60

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer.read()