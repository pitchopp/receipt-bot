from django.db import models


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
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.apartment} - {self.tenant}"