from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *

# --- AUTHENTICATION ---

def index(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "index.html", {'error': "Invalid credentials", 'settings': ShopSettings.objects.first()})
    return render(request, "index.html", {'settings': ShopSettings.objects.first()})


@login_required
def logout_view(request):
    logout(request)
    return redirect("index")


# --- DASHBOARD ---

@login_required
def dashboard(request):
    return render(request, "dashboard.html")


# --- PRODUCTS & INVENTORY ---

@login_required
def product_list(request):
    return render(request, "products/product_list.html")

@login_required
def add_product(request):
    return render(request, "products/add_product.html")

@login_required
def stock_management(request):
    return render(request, "products/stock.html")


# --- SALES & BILLING ---

@login_required
def new_sale(request):
    return render(request, "sales/new_sale.html")

@login_required
def sales_history(request):
    return render(request, "sales/sales_history.html")

@login_required
def gst_invoices(request):
    return render(request, "sales/gst_invoices.html")


# --- CUSTOMERS ---

@login_required
def customer_list(request):
    return render(request, "customers/customer_list.html")


# --- TAILORING ORDERS ---

@login_required
def order_list(request):
    return render(request, "orders/order_list.html")

@login_required
def new_order(request):
    return render(request, "orders/new_order.html")

@login_required
def measurement_list(request):
    return render(request, "orders/measurement_list.html")


# --- EMPLOYEES ---

@login_required
def employee_list(request):
    return render(request, "employees/employee_list.html")

@login_required
def attendance(request):
    return render(request, "employees/attendance.html")

@login_required
def leaves(request):
    return render(request, "employees/leaves.html")


# --- EXPENSES ---

@login_required
def expense_list(request):
    return render(request, "expenses/expense_list.html")


# --- REPORTS ---

@login_required
def sales_report(request):
    return render(request, "reports/sales_report.html")

@login_required
def inventory_report(request):
    return render(request, "reports/inventory_report.html")

@login_required
def profit_report(request):
    return render(request, "reports/profit_report.html")


# --- SETTINGS ---

@login_required
def shop_settings(request):
    return render(request, "settings/shop_settings.html")

@login_required
def theme_settings(request):
    return render(request, "settings/theme_settings.html")

@login_required
def backup_restore(request):
    return render(request, "settings/backup_restore.html")
