import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
from .settings import Settings
from assistant.models import Receipt


def send_receipt(receipt: Receipt, settings: Settings = Settings()):
    # Define the email subject and body
    month = receipt.month
    tenant = receipt.payment.contract.tenant
    pdf_file = receipt.document.path
    subject = 'Quittance de loyer ' + month.strftime("%B %Y")
    body = 'Bonjour ' + tenant.first_name + ',\n\nVeuillez trouver ci-joint la quittance de loyer pour le mois de ' + month.strftime("%B %Y") + '.\n\nCordialement,\n\nChella Dior'
    recipient = tenant.email_address
    
    # Create a multipart message object and set the headers
    msg = MIMEMultipart()
    msg['From'] = settings.sender_email
    msg['To'] = COMMASPACE.join([recipient])
    msg['Subject'] = subject

    # Add the email body to the message
    msg.attach(MIMEText(body, 'plain'))

    # Open the PDF file in binary mode and attach it to the message
    with open(pdf_file, 'rb') as f:
        pdf_data = f.read()
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(pdf_data)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename='quittance.pdf')
        msg.attach(part)

    with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(settings.smtp_username, settings.smtp_password)
        smtp.sendmail(settings.sender_email, recipient, msg.as_string())
