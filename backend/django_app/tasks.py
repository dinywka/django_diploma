from celery import shared_task
from django.core.mail import EmailMessage, get_connection
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Product

def generate_pdf(products, buffer):
    # Create PDF
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(100, 800, "Product List")

    y_position = 780
    for product in products:
        y_position -= 20
        pdf.drawString(100, y_position, f"Name: {product.name}")
        y_position -= 15
        pdf.drawString(100, y_position, f"Description: {product.description}")
        y_position -= 15
        pdf.drawString(100, y_position, f"Price: ${product.price}")

    pdf.save()

    # Move buffer position to the beginning
    buffer.seek(0)

    return buffer.getvalue()

@shared_task
def generate_and_email_pdf():
    buffer = BytesIO()
    products = Product.objects.all()
    generate_pdf(products, buffer)

    connection = get_connection('django.core.mail.backends.smtp.EmailBackend')
    connection.open()

    email = EmailMessage(
        'Daily Product Report',
        'See attached PDF for the list of products.',
        'dina.kulmagambetova@yandex.kz',
        ['dina_kul@mail.ru'],
        connection=connection,
    )

    email.attach(filename='daily_product_report.pdf', content=buffer.getvalue(), mimetype='application/pdf')
    email.send()
    connection.close()
