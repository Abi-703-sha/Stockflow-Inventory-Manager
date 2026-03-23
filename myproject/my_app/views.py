from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Stock, StockTransaction, UserProfile
from .forms import SignUpForm, StockForm, StockTransactionForm, UserAddForm

def home(request):
return render(request, 'my_app/home.html')

def about_view(request):
return render(request, 'my_app/about.html')

def help_view(request):
return render(request, 'my_app/help.html')

def signup_view(request):
if request.method == 'POST':
form = SignUpForm(request.POST)
if form.is_valid():
form.save()
messages.success(request, "Account created successfully! Please login.")
return redirect('login')
else:
form = SignUpForm()
return render(request, 'my_app/signup.html', {'form': form})

def login_view(request):
if request.method == 'POST':
form = AuthenticationForm(request, data=request.POST)
if form.is_valid():
username = form.cleaned_data.get('username')
password = form.cleaned_data.get('password')
user = authenticate(username=username, password=password)
if user is not None:
login(request, user)
return redirect('dashboard')
else:
messages.error(request, "Invalid username or password.")
else:
messages.error(request, "Invalid username or password.")
else:
form = AuthenticationForm()
return render(request, 'my_app/login.html', {'form': form})

@login_required
def dashboard(request):
stocks = Stock.objects.all()
total_products = stocks.count()
low_stock_count = stocks.filter(quantity__lt=10).count()
out_of_stock = stocks.filter(quantity=0).count()

if low_stock_count > 0:
if out_of_stock > 0:
messages.warning(request, f"Critical Inventory Alert: {low_stock_count} items are below 10 units (including {out_of_stock} out of stock)!")
else:
messages.warning(request, f"Low Stock Alert: {low_stock_count} items are below 10 units!")

context = {
'stocks': stocks,
'total_products': total_products,
'low_stock': low_stock_count,
'out_of_stock': out_of_stock,
}
return render(request, 'my_app/dashboard.html', context)

@login_required
def inventory_list(request):
stocks = Stock.objects.all()
low_stock_count = stocks.filter(quantity__lt=10, quantity__gt=0).count()
if low_stock_count > 0:
messages.warning(request, f"Attention: {low_stock_count} items in your inventory are running low (below 10 units)!")

return render(request, 'my_app/inventory_list.html', {'stocks': stocks})

@login_required
def add_stock(request):
stocks = Stock.objects.all()
if request.method == 'POST':
form = StockForm(request.POST)
if form.is_valid():
stock = form.save()
messages.success(request, "Stock added successfully!")
if stock.quantity < 10:
messages.warning(request, f"Note: {stock.name} was added with low stock ({stock.quantity} units).")
return redirect('add_stock')
else:
form = StockForm()
return render(request, 'my_app/add_stock.html', {'form': form, 'stocks': stocks})

@login_required
def update_stock(request, pk):
stock = get_object_or_404(Stock, pk=pk)
if request.method == 'POST':
form = StockForm(request.POST, instance=stock)
if form.is_valid():
stock = form.save()
messages.success(request, "Stock updated successfully!")
if 0 < stock.quantity < 10:
messages.warning(request, f"Note: {stock.name} is now in low stock ({stock.quantity} units).")
elif stock.quantity == 0:
messages.error(request, f"Alert: {stock.name} is now out of stock!")
return redirect('dashboard')
else:
form = StockForm(instance=stock)
return render(request, 'my_app/update_stock.html', {'form': form, 'stock': stock})

@login_required
def delete_stock(request, pk):
stock = get_object_or_404(Stock, pk=pk)
if request.method == 'POST':
stock.delete()
messages.success(request, "Stock deleted successfully!")
return redirect('dashboard')
return render(request, 'my_app/delete_stock.html', {'stock': stock})

@login_required
def view_stock(request, pk):
stock = get_object_or_404(Stock, pk=pk)
return render(request, 'my_app/view_stock.html', {'stock': stock})

@login_required
def stock_management(request):
return render(request, 'my_app/stock_management.html')

@login_required
def stock_in(request):
if request.method == 'POST':
form = StockTransactionForm(request.POST)
if form.is_valid():
transaction = form.save(commit=False)
transaction.transaction_type = 'IN'
transaction.save()

# Update product quantity
product = transaction.product
product.quantity += transaction.quantity
product.save()

messages.success(request, f"Successfully added {transaction.quantity} to {product.name}.")
return redirect('stock_history')
else:
form = StockTransactionForm()
return render(request, 'my_app/stock_in.html', {'form': form})

@login_required
def stock_out(request):
if request.method == 'POST':
form = StockTransactionForm(request.POST)
if form.is_valid():
transaction = form.save(commit=False)
transaction.transaction_type = 'OUT'

product = transaction.product
if product.quantity >= transaction.quantity:
transaction.save()
product.quantity -= transaction.quantity
product.save()

messages.success(request, f"Successfully removed {transaction.quantity} from {product.name}.")

if product.quantity < 10:
    messages.warning(request, f"Critical Alert: {product.name} has dropped to {product.quantity} units!")
    
return redirect('stock_history')
else:
messages.error(request, f"Insufficient stock for {product.name}. Current quantity: {product.quantity}")
else:
form = StockTransactionForm()
return render(request, 'my_app/stock_out.html', {'form': form})

@login_required
def stock_history(request):
history = StockTransaction.objects.all().order_by('-created_at')
return render(request, 'my_app/stock_history.html', {'history': history})

@login_required
def user_management(request):
users = User.objects.all().select_related('userprofile')
return render(request, 'my_app/user_management.html', {'users': users})

@login_required
def add_user(request):
if request.method == 'POST':
form = UserAddForm(request.POST)
if form.is_valid():
user = form.save(commit=False)
user.set_password(form.cleaned_data['password'])
user.save()

# Create profile
UserProfile.objects.create(
user=user,
role=form.cleaned_data['role']
)

messages.success(request, f"User {user.username} added successfully.")
return redirect('user_management')
else:
form = UserAddForm()
return render(request, 'my_app/add_user.html', {'form': form})

def logout_view(request):
logout(request)
return redirect('login')
