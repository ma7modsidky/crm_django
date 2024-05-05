from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, SignUpForm, CustomerForm, CompanyForm
from . models import Customer, Company , Deal, Task
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
# Create your views here.

def home(request):
    return render(request, 'website/home.html', {})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you have been logged in successfully')
                return redirect('home')
            else:
                messages.error(request, 'There was an error, please try again')
                return render(request, 'website/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'website/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'website/register.html', {'form':form})

	return render(request, 'website/register.html', {'form':form})


# Customer Views
# Function Based Views
def customer_list(request):
    """Display a list of customers."""
    customers = Customer.objects.all()
    # Set the number of items per page
    items_per_page = 4
    
    # Create a Paginator instance
    paginator = Paginator(customers, items_per_page)
    
    # Get the current page number from the request
    page_number = request.GET.get('page')
    
    # Get the Page object for the current page
    page = paginator.get_page(page_number)
    
    return render(request, 'website/customer/customer_list.html', {'page': page})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'website/customer/customer_detail.html' , {"customer": customer})

def customer_update(request, pk):
    """
    Update customer details.
    """
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', pk=customer.pk)  # Redirect to customer detail page
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'website/customer/customer_update.html', {'form': form, 'customer': customer})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'you have created a new customer successfully')
            return redirect('customer_list')  # Redirect to the customer list view
    else:
        form = CustomerForm()

    return render(request, 'website/generics/create_edit_form.html', {'form': form})

# Company Views
# Class Based Views
class CompanyList(ListView):
    """Display a list of comapnies."""
    model = Company
    template_name = 'website/company/company_list.html'
    paginate_by = 3


class CompanyDetail(DetailView):    
    model = Company
    template_name = 'website/company/company_detail.html'
    context_object_name = 'company'
    
    
class CompanyCreate(CreateView):
    model = Company
    # fields = "__all__"  # Specifing fields and form class is not permitted
    form_class = CompanyForm
    template_name = 'website/generics/create_edit_form.html'
    

class CompanyDelete(DeleteView):
    model = Company
    success_url = reverse_lazy('company_list') # Redirect after successful deletion

    # def get_object(self, queryset=None):
    #     # Optional: Check ownership or permissions here
    #     obj = super().get_object()
    #     # Add your custom logic (e.g., check if the user owns the company)
    #     return obj