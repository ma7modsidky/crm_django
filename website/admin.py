from django.contrib import admin
from .models import Customer, Company, Deal, Task
# Register your models here.

admin.site.register(Customer)
admin.site.register(Company)
admin.site.register(Deal)
admin.site.register(Task)


