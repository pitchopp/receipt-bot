import base64
import pdfkit
from jinja2 import Environment, FileSystemLoader
from assistant import models
from datetime import date
import locale
from dateutil.relativedelta import relativedelta
from decimal import Decimal
import os

class InactiveContractException(Exception):
    """Exception raised when a contract is not active."""


def get_image_file_as_base64_data():
    with open("assistant/static/logo.png", 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def calculate_coef_amount(month, period_start_date, period_end_date) -> Decimal:
    month_days = ((month.replace(day=1) + relativedelta(months=1, days=-1)) - month.replace(day=1)).days + 1
    nb_days = (period_end_date - period_start_date).days + 1
    coef = Decimal(nb_days / month_days)
    return coef


def generate_receipt(contract: models.Contract, payment_date: date, month: date, period_start: date, period_end: date):
    amount = contract.rent + contract.charges

    coef = calculate_coef_amount(month, period_start, period_end)
    
    # Create a Jinja environment with the template directory
    env = Environment(loader=FileSystemLoader('assistant/templates'))

    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

    # Define the variables to replace in the template
    variables = {
        'logo_base64': get_image_file_as_base64_data(),
        'contract': contract,
        'rent': contract.rent * coef,
        'charges': contract.charges * coef,
        'total_amount': coef * amount,
        'payment_date': payment_date,
        # make month in french
        'month': f"{month:%B %Y}",  # "January 2020
        'period_start': period_start,
        'period_end': period_end
    }

    # Load the template from a file
    template = env.get_template('quittance.html.j2')

    # Render the template with the variables replaced by their values
    output = template.render(variables)
    filename = f"quittance_{contract.tenant.first_name}_{contract.tenant.last_name}_{month:%B %Y}.pdf"
    folder = 'media/receipts'
    # create folder media/receipts if it doesn't exist
    if not os.path.isdir('media'):
        os.mkdir('media')
    if not os.path.isdir(folder):
        os.mkdir(folder)
    file_path = os.path.join(folder, filename)
    pdfkit.from_string(output, file_path, options={"enable-local-file-access": ""})
    return file_path[len('media')+1:]
