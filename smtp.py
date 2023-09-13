import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

# Define the sender and recipient email addresses
sender = 'noreply@chella.tech'
recipient = 'sghir.ma@gmail.com'

# Define the email subject and body
subject = 'PDF attachment'
body = 'Please find attached the PDF file.'

# Define the path to the PDF file
pdf_file = 'output.pdf'

# Define the Zoho server and port
server = 'smtp.zoho.com'
port = 465

# Define your Zoho email account credentials
username = 'amine.sghir@chella.tech'
password = 'VnCdE28u'

# Create a multipart message object and set the headers
msg = MIMEMultipart()
msg['From'] = sender
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

# Connect to the Zoho server and send the message
with smtplib.SMTP(server, port) as smtp:
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(sender, recipient, msg.as_string())