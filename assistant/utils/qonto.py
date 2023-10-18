import requests
from urllib.parse import urljoin
from assistant.utils.settings import Settings
from datetime import date as dt

class QontoApi:
    def __init__(self, client_id=None, secret_key=None, iban=None) -> None:
        settings = Settings()
        self.client_id = client_id if client_id else settings.qonto_client_id
        self.secret_key = secret_key if secret_key else settings.qonto_secret_key
        self.iban = iban if iban else settings.qonto_iban
        self.base_url = 'https://thirdparty.qonto.com/v2/'
        self.transactions_path = 'transactions'
    
    def _get(self, path: str, params: dict = None):
        url = self.base_url + path
        url += '?' + '&'.join([f'{k}={v}' for k, v in params.items()]) if params else ''
        headers = {
            'Authorization': f"{self.client_id}:{self.secret_key}"
        }
        return requests.get(url, headers=headers)
    
    def get_transactions(self, **kwargs):
        params = kwargs.copy()
        if 'iban' not in params:
            params['iban'] = self.iban
        return self._get(self.transactions_path, params).json()
