"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from my_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('help/', views.help_view, name='help'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('stock/add/', views.add_stock, name='add_stock'),
    path('stock/view/<int:pk>/', views.view_stock, name='view_stock'),
    path('stock/update/<int:pk>/', views.update_stock, name='update_stock'),
    path('stock/delete/<int:pk>/', views.delete_stock, name='delete_stock'),
    
    # Stock Management
    path('stock-management/', views.stock_management, name='stock_management'),
    path('stock-in/', views.stock_in, name='stock_in'),
    path('stock-out/', views.stock_out, name='stock_out'),
    path('stock-history/', views.stock_history, name='stock_history'),
    
    # User Management
    path('user-management/', views.user_management, name='user_management'),
    path('user/add/', views.add_user, name='add_user'),
    
    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='my_app/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='my_app/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='my_app/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='my_app/password_reset_complete.html'), name='password_reset_complete'),
]
