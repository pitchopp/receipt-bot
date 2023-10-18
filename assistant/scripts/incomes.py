from datetime import datetime, timezone
import traceback
from assistant.utils.transactions import Income, get_incomes
from assistant.models import Contract, Task, Receipt, Payment
from tqdm import tqdm
from assistant.utils.generator import calculate_coef_amount, generate_receipt
from assistant.utils.smtp import send_receipt
from datetime import date
from dateutil.relativedelta import relativedelta


class ContractException(Exception):
    pass



def identify_contract(income: Income) -> Contract:
    contract = Contract.objects.filter(tenant_iban=income.from_iban)
    # if we find more than one contract, alert the user
    if len(contract) > 1:
        raise ContractException(f"multiple contracts found for {income.from_iban}")
    # if no contract is found, alert the user
    if len(contract) == 0:
        raise ContractException(f"no contract found for {income.from_iban}")    
    contract = contract.first()
    return contract


def calculate_expected_echeance(contract: Contract) -> tuple[float, date, date]:
    """Calculate the expected amount for a given contract."""
    # First we need to find the last receipt
    all_receipts = Receipt.objects.filter(payment__contract=contract).order_by('month')
    base_amount = contract.amount
    if len(all_receipts) == 0:
        period_start = contract.start_date
        period_end = contract.start_date.replace(day=1) + relativedelta(months=1, days=-1)
    else:
        last_receipt = all_receipts.last()
        # calculate the period_start and period_end
        period_start = (last_receipt.month + relativedelta(months=1)).replace(day=1)
        period_end = period_start + relativedelta(months=1, days=-1)
    
    if contract.end_date and contract.end_date < period_end:
        period_end = contract.end_date
    # calculate the amount
    coef = calculate_coef_amount(period_start, period_start, period_end)
    amount = round(coef * base_amount, 2)
    return amount, period_start, period_end


def main(task: Task):
    # First we retrieve the incomes
    incomes = get_incomes()
    for income in tqdm(sorted(incomes, key=lambda x: x.settled_at), desc='incomes'):
        # try to find a contract with the same iban
        
        try:
            contract = identify_contract(income)
        except ContractException as e:
            print(str(e))
            continue
        
        amount, period_start, period_end = calculate_expected_echeance(contract)
        print(amount, period_start, period_end)
        # verify that the amount is correct
        if income.amount != amount:
            print(f"wrong amount for {income.from_iban}")
            continue
        
        
        # create a receipt for this income
        quittance = generate_receipt(
            contract=contract,
            payment_date=income.settled_at,
            month=income.settled_at,
            period_start=period_start,
            period_end=period_end
        )
        payment = Payment.objects.create(
            bank_id=income.id,
            date=income.settled_at,
            amount=income.amount,
            contract=contract
        )
        receipt = Receipt.objects.create(
            month=income.settled_at,
            period_start=period_start,
            period_end=period_end,
            payment=payment,
            document=quittance,
            source_task=task
        )
        # send quittance by mail
        send_receipt(receipt)
        



def run(*args):
    """This job aims to retrieve all the incomes received since the last time it was run and create a receipt for each of them."""
    # Create a task for this job
    task = Task.objects.create(name='incomes', status='running')
    try:
        main(task)
    except Exception as e:
        task.status = 'failed'
        task.error = str(e)
        task.traceback = traceback.format_exc()
        task.end_date = datetime.now(tz=timezone.utc)
        task.save()
        raise e
    else:
        task.status = 'success'
        task.end_date = datetime.now(tz=timezone.utc)
        task.save()