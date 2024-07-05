from django.urls import path
from . import views 
urlpatterns = [
    path('', views.home, name='home'),
    # Authentication Urls
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    # Crm Urls
    # Customer Urls
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:pk>/modify/', views.customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('customers/<int:customer_id>/deals/', views.CustomerDealsListView.as_view(), name='customer_deals_list'),
    
    # Company Urls
    path('companies/', views.CompanyList.as_view(), name='company_list'),
    path('companies/<int:pk>/', views.CompanyDetail.as_view(), name='company_detail'),
    path('companies/create/', views.CompanyCreate.as_view(), name='company_create'),
    path('companies/<int:pk>/modify/', views.CompanyUpdate.as_view(), name='company_update'),
    path('companies/<int:pk>/delete/', views.CompanyDelete.as_view(), name='company_delete'),
    # Users Urls
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    # Deals Urls
    path('deals/', views.DealList.as_view(), name='deal_list'),
    path('deals/create/', views.DealCreate.as_view(), name='deal_create'),
]
