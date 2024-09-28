from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, SignUpForm, CustomerForm, CompanyForm, DealForm
from . models import Customer, Company , Deal, Task
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return render(request, 'website/home.html', {})
    else:
        return redirect('login')
    

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you have been logged in successfully')
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
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
    items_per_page = 10
    
    # Create a Paginator instance
    paginator = Paginator(customers, items_per_page)
    
    # Get the current page number from the request
    page_number = request.GET.get('page')
    
    # Get the Page object for the current page
    page = paginator.get_page(page_number)
    
    return render(request, 'website/customer/customer_list.html', {'page': page})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    latest_deals = Deal.objects.filter(customer=customer).order_by('-created_at')[:5]
    return render(request, 'website/customer/customer_detail.html' , {"customer": customer, "deals": latest_deals})

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

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, f'Customer {customer.name} successfully deleted.')
        return redirect('customer_list')  # Redirect to the list of customers

    context = {
        'object': customer
    }
    return render(request, 'website/generics/confirm_delete.html', context)


# Company Views
# Class Based Views
class CompanyList(LoginRequiredMixin,ListView):
    """Display a list of comapnies."""
    model = Company
    template_name = 'website/company/company_list.html'
    paginate_by = 3


class CompanyDetail(LoginRequiredMixin,DetailView):    
    model = Company
    template_name = 'website/company/company_detail.html'
    context_object_name = 'company'
    
    
class CompanyCreate(LoginRequiredMixin,CreateView):
    model = Company
    # fields = "__all__"  # Specifing fields and form class is not permitted
    form_class = CompanyForm
    template_name = 'website/generics/create_edit_form.html'
    

class CompanyUpdate(LoginRequiredMixin,UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'website/generics/create_edit_form.html'
    
class CompanyDelete(LoginRequiredMixin,DeleteView):
    model = Company
    success_url = reverse_lazy('company_list') # Redirect after successful deletion

    # def get_object(self, queryset=None):
    #     # Optional: Check ownership or permissions here
    #     obj = super().get_object()
    #     # Add your custom logic (e.g., check if the user owns the company)
    #     return obj

# User Views

class UserList(LoginRequiredMixin,ListView):
    model = User
    template_name = 'website/user/user_list.html'
    paginate_by = 10
    

class UserDetail(LoginRequiredMixin,DetailView):    
    model = User
    template_name = 'website/user/user_detail.html'
    context_object_name = 'user'    
    
# Deals

class DealList(LoginRequiredMixin,ListView):
    model = Deal
    template_name = 'website/deal/deal_list.html'
    context_object_name = 'deals'

class CustomerDealsListView(LoginRequiredMixin,ListView):
    model = Deal
    template_name = 'website/deal/deal_list_customer.html'
    context_object_name = 'deals'    
    
    def get_queryset(self):
        # Retrieve the customer ID from the URL parameter (e.g., /customer/1/deals/)
        customer_id = self.kwargs.get('customer_id')  # Assuming you use 'customer_id' as the parameter name

        # Get the customer object based on the ID
        customer = Customer.objects.get(pk=customer_id)

        # Retrieve all deals associated with this customer
        return Deal.objects.filter(customer=customer)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the customer instance to the context
        customer_id = self.kwargs.get('customer_id')
        customer = Customer.objects.get(pk=customer_id)
        context['customer'] = customer  # Replace 'customer' with the actual variable name
        return context
class DealCreate(LoginRequiredMixin,CreateView):
    model = Deal
    form_class = DealForm
    template_name = 'website/generics/create_edit_form.html'
    success_url = reverse_lazy('deal_list')
    
    def get_initial(self):
        initial = super().get_initial()
        # Assuming you have a foreign key field named 'customer' in your DealForm
        # You can replace 'customer_id' with the actual field name in your form
        if self.kwargs.get('customer_id'):
            customer_id = self.kwargs.get('customer_id')  # Get the customer ID from the URL
            customer = get_object_or_404(Customer, pk=customer_id)
            initial['customer'] = customer
        return initial
    
    def get_success_url(self):
        customer_id = self.kwargs.get('customer_id')
        if customer_id:
            customer = get_object_or_404(Customer, pk=customer_id)
            # Redirect to a specific customer detail page
            return reverse_lazy('customer_detail', kwargs={'pk': customer_id})
        else:
            # Redirect to a generic list view (e.g., deal_list)
            return reverse_lazy('deal_list')
    
class DealDetail(LoginRequiredMixin,DetailView):
    model = Deal
    template_name = 'website/deal/deal_detail.html'

class DealUpdate(LoginRequiredMixin,UpdateView):
    model = Deal
    form_class = DealForm
    template_name = 'website/generics/create_edit_form.html'
    
class DealDelete(LoginRequiredMixin,DeleteView):
    model = Deal
    success_url = reverse_lazy('deal_list') # Redirect after successful deletion
    
    def get_success_url(self):
        customer_id = self.kwargs.get('customer_id')
        if customer_id:
            customer = get_object_or_404(Customer, pk=customer_id)
            # Redirect to a specific customer detail page
            return reverse_lazy('customer_detail', kwargs={'pk': customer_id})
        else:
            # Redirect to a generic list view (e.g., deal_list)
            return reverse_lazy('deal_list')