import base64
import pdfkit
from jinja2 import Environment, FileSystemLoader
from assistant import models
from datetime import date
import locale
from dateutil.relativedelta import relativedelta

class InactiveContractException(Exception):
    """Exception raised when a contract is not active."""


def get_image_file_as_base64_data():
    with open("assistant/static/logo.png", 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def generate_receipt(contract: models.Contract, payment_date: date, month: date):
    
    period_start = month.replace(day=1)
    period_end = month.replace(day=1) + relativedelta(months=1, days=-1)
    
    # check if the contract is active
    if contract.start_date > period_end or (contract.end_date and contract.end_date < period_start):
        raise Exception('Contract is not active')
    

    # Create a Jinja environment with the template directory
    env = Environment(loader=FileSystemLoader('assistant/templates'))

    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

    # Define the variables to replace in the template
    variables = {
        'logo_base64': get_image_file_as_base64_data(),
        'contract': contract,
        'payment_date': payment_date,
        # make month in french
        'month': f"{month:%B %Y}",  # "January 2020
        'period_start': period_start,
        'period_end': period_end
    }

    # Load the template from a file
    template = env.get_template('quittance.html')

    # Render the template with the variables replaced by their values
    output = template.render(variables)
    filename = f"quittance_{contract.tenant.first_name}_{contract.tenant.last_name}_{month:%B %Y}.pdf"
    pdfkit.from_string(output, f'output/{filename}', options={"enable-local-file-access": ""})
    return f'output/{filename}'
