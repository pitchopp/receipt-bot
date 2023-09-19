import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'receipt_bot.settings')
django.setup()
from datetime import date
from assistant.utils.generator import generate_receipt
from assistant.models import Contract
from assistant.utils.smtp import send_receipt


if __name__ == "__main__":
    # contract = Contract.objects.filter(tenant__first_name='Jules').first()
    contract = Contract.objects.filter(tenant__first_name='Steven').first()
    quittance = generate_receipt(contract=contract, payment_date=date(2023, 9, 5), month=date(2023, 9, 1))
    # send quittance by mail
    # send_receipt(contract.tenant, date(2023, 9, 1), quittance)
