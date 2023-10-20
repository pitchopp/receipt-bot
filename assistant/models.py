from django.db import models
# from .utils.smtp import send_receipt
# from .utils.generator import generate_receipt


class Apartment(models.Model):
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    
    @property
    def full_address(self):
        return f"{self.number} {self.street}, {self.postal_code} {self.city}, {self.country}"
    
    def __str__(self):
        return self.name


class Tenant(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.EmailField()
    phone = models.CharField(max_length=20)
    iban = models.CharField(max_length=34, null=True, blank=True)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Contract(models.Model):
    TYPE_CHOICES = [
        ('CBI', 'Colocation Bail Individuel'),
        ('CBS', 'Colocation Bail Solidaire'),
    ]
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    charges = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE)
    tenant_iban = models.CharField(max_length=34, null=True, blank=True)
    
    
    @property
    def amount(self):
        return self.rent + self.charges
    
    def __str__(self) -> str:
        return f"{self.apartment} - {self.tenant}"

class Payment(models.Model):
    transaction_id = models.CharField(max_length=255)
    bank = models.CharField(max_length=50, choices=[
        ('qonto', 'Qonto'),
    ])
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, blank=True)
    is_rent = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.contract} - {self.date}"

class Receipt(models.Model):
    generation_date = models.DateField(auto_now_add=True)
    month = models.DateField()
    period_start = models.DateField()
    period_end = models.DateField()
    document = models.FileField(upload_to='receipts')
    payment = models.OneToOneField('Payment', on_delete=models.SET_NULL, null=True, blank=True)
    source_task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True, blank=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.contract} - {self.month}"

class Task(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[
        ('running', 'Running'),
        ('success', 'Success'),
        ('error', 'Error'),
    ], default='running')
    error = models.TextField(null=True, blank=True)
    traceback = models.TextField(null=True, blank=True)
    
    
    def __str__(self) -> str:
        return f"{self.name} - {self.start_date}"
    