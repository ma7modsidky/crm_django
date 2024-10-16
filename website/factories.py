import factory
from factory.django import DjangoModelFactory
from faker import Faker

from . models import Customer, Company , Deal

fake = Faker()
class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer
        
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    phone_number = factory.Faker('phone_number')
    email = factory.lazy_attribute(lambda obj: f"{obj.first_name.lower()}.{obj.last_name.lower()}.{fake.unique.random_int(1,9999)}@example.com")
    address = factory.Faker('address')
    country = factory.Faker('country')
    state = factory.Faker('state')
    city = factory.Faker('city')
    
    
class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company
    
    name = factory.Faker('company')
    industry = factory.Faker('sentence', nb_words=2)
    website = factory.lazy_attribute(lambda obj: f"www.{obj.name.lower().replace(' ', '.')}.com")
    
    
    
          
    