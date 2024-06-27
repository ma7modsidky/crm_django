from django.db import models
from django.urls import reverse
# Create your models here.

# class ContactInfo(models.Model):
#     phone_number = models.CharField(max_length=20)
#     phone_number_2 = models.CharField(max_length=20,blank=True, null=True)
#     email = models.EmailField(unique=True)
#     address = models.TextField(blank=True, null=True)
#     country = models.CharField(max_length=100)
#     state = models.CharField(max_length=100, blank=True, null=True)
#     city = models.CharField(max_length=100, blank=True, null=True)
#     zip_code = models.CharField(max_length=100, blank=True, null=True)
class Customer(models.Model):
    """
    Represents a customer in the CRM system.
    """
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100,blank=True, null=True)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    phone_number_2 = models.CharField(max_length=20,blank=True, null=True)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def name(self):
        return self.first_name +" "+ self.last_name
class Company(models.Model):
    """
    Represents a company in the CRM system.
    """
    name = models.CharField(max_length=200, unique=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("company_detail", kwargs={"pk": self.pk})
    

class Deal(models.Model):
    """
    Represents a deal or opportunity in the CRM system.
    """
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stage = models.CharField(max_length=50, choices=[
        ('prospect', 'Prospect'),
        ('qualified', 'Qualified'),
        ('negotiation', 'Negotiation'),
        ('closed', 'Closed'),
    ])
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    
class Task(models.Model):
    """
    Represents a task or to-do item related to a customer or deal.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title