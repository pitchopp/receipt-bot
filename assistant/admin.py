from django.contrib import admin
from .models import Apartment, Tenant, Contract, Receipt, Task, Payment
# Register your models here.

admin.site.register(Apartment)
admin.site.register(Tenant)
admin.site.register(Contract)
admin.site.register(Receipt)
admin.site.register(Task)
admin.site.register(Payment)
