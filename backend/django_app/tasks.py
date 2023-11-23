from celery import shared_task
from django.core.mail import EmailMessage, get_connection
from reportlab.pdfgen import canvas
from .models import Product
from io import BytesIO

@shared_task
def generate_and_email_pdf():
    buffer = BytesIO()
    generate_pdf(buffer)

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

def generate_pdf(buffer):
    p = canvas.Canvas(buffer)
    products = Product.objects.all()
    for product in products:
        p.drawString(100, 100, f"Product: {product.name}, Price: {product.price}")
    p.showPage()
    p.save()
    buffer.seek(0)
