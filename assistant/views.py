from django.shortcuts import render
from .models import Contract
from datetime import date

def active_contracts(request):
    today = date.today()
    active_contracts = Contract.objects.filter(start_date__lte=today, end_date__gte=today) | Contract.objects.filter(start_date__lte=today, end_date__isnull=True)
    context = {'contracts': active_contracts}
    return render(request, 'active_contracts.html.j2', context, using='jinja2')