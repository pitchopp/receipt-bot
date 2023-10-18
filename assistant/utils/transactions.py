from .qonto import QontoApi
from datetime import datetime
from pydantic import BaseModel


api = QontoApi()


class Income(BaseModel):
    """positive transaction model"""
    id: str
    amount: int
    currency: str
    settled_at: datetime
    reference: str
    from_iban: str
    
    @classmethod
    def from_transaction(cls, transaction: dict) -> 'Income':
        assert transaction['subject_type'] == 'Income'
        assert 'income' in transaction
        assert transaction['status'] == 'completed'
        assert transaction['currency'] == 'EUR'
        assert transaction['side'] == 'credit'
        assert transaction['income']['counterparty_account_number_format'] == 'IBAN'
        return cls(
            id=transaction['id'],
            amount=transaction['amount'],
            currency=transaction['currency'],
            settled_at=transaction['settled_at'],
            reference=transaction['reference'],
            from_iban=transaction['income']['counterparty_account_number']
        )
    
    @classmethod
    def from_transactions(cls, transactions: list[dict]) -> list['Income']:
        return [cls.from_transaction(t) for t in transactions]
    
    

def get_incomes(start_date: datetime = None, end_date: datetime = None):
    params = {
        'side': 'credit',
        'per_page': 100
    }
    if start_date:
        params['settled_at_from'] = start_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    if end_date:
        params['settled_at_to'] = end_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    incomes = api.get_transactions(**params)['transactions']
    incomes = [i for i in incomes if i['subject_type'] == 'Income' and 'income' in i]
    return Income.from_transactions(incomes)
    


if __name__ == '__main__':
    print('hello world')