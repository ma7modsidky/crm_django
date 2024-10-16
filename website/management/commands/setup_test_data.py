import random

from django.db import transaction
from django.core.management.base import BaseCommand

from website.models import Customer, Company
from website.factories import CustomerFactory, CompanyFactory

NUM_CUSTOMERS = 100
NUM_COMPANIES = 5

class Command(BaseCommand):
    help = 'Generate some test data'
    
    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data ...\n')
        models = [Customer, Company]
        # for m in models:
        #     m.objects.all().delete()
            
        self.stdout.write('Generating new data...\n')   
        # create customers
        # CustomerFactory.create_batch(NUM_CUSTOMERS)
        CompanyFactory.create_batch(NUM_COMPANIES)
        self.stdout.write('Data created successfuly\n')        
    