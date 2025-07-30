from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
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
    settings=ShopSettings.objects.first()
    return render(request, "dashboard.html",{"settings":settings})


# --- PRODUCTS & INVENTORY ---

@login_required
def product_list(request):
    settings = ShopSettings.objects.first()
    products=tbl_Product.objects.all()
    context={
        "settings":settings,
        "products":products,
    }
    return render(request, "products/product_list.html",context)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')  # Your product list URL
    else:
        settings = ShopSettings.objects.first()
        form = ProductForm()
    return render(request, "products/add_product.html",{'form':form,
                                                        'settings':settings})

@login_required
def stock_management(request):
    return render(request, "products/stock.html")

@login_required
def product_categories(request):
    settings=ShopSettings.objects.first()
    category=tbl_Category.objects.all()
    context={
        "category":category,
        "settings":settings
    }
    return render(request, "products/categories.html",context)

@login_required
def sub_categories(request):
    settings=ShopSettings.objects.first()
    sub=tbl_SubCategory.objects.all()
    context={
        "sub":sub,
        "settings":settings
    }
    return render(request, "products/sub_categories.html",context)
@login_required
def category_add(request):
    if request.method == "POST":
        form = ProductCategoriesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_categories')
    else:
        settings = ShopSettings.objects.first()
        form = ProductCategoriesForm()
    return render(request, "products/category_add.html", {"form": form,"settings":settings})

def subcategory_add(request):
    if request.method == "POST":
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sub_categories')
    else:
        settings = ShopSettings.objects.first()
        form = SubCategoryForm()
    return render(request, "products/subcategory_add.html", {"form": form,"settings":settings})

# --- SALES ---

@login_required
def new_sale(request):
    return render(request, "sales/new_sale.html")

@login_required
def sales_history(request):
    return render(request, "sales/sales_history.html")


# --- PURCHASES ---

@login_required
def new_purchase(request):
    if request.method == "POST":
        vendor_id = request.POST.get('vendor')
        invoice = request.POST.get('invoice_number')
        date = request.POST.get('purchase_date')
        mode = request.POST.get('payment_mode')
        status = request.POST.get('payment_status')
        notes = request.POST.get('notes')

        try:
            with transaction.atomic():
                purchase = Purchase.objects.create(
                    vendor_id=vendor_id,
                    invoice_number=invoice,
                    purchase_date=date,
                    payment_mode=mode,
                    payment_status=status,
                    notes=notes
                )

                product_names = request.POST.getlist('product_name')
                brands = request.POST.getlist('brand')
                categories = request.POST.getlist('category')
                subcategories = request.POST.getlist('subcategory')
                quantities = request.POST.getlist('quantity')
                prices = request.POST.getlist('unit_price')
                gst_percents = request.POST.getlist('gst_percentage')

                for i in range(len(product_names)):
                    product, created = tbl_Product.objects.get_or_create(
                        name=product_names[i],
                        brand=brands[i],
                        category=categories[i],
                        subcategory=subcategories[i],
                        defaults={
                            'price': prices[i],
                            'stock': 0,
                            'status': 'active'
                        }
                    )

                    product.stock += int(quantities[i])
                    product.save()

                    PurchaseItem.objects.create(
                        purchase=purchase,
                        product=product,
                        quantity=quantities[i],
                        unit_price=prices[i],
                        gst_percentage=gst_percents[i]
                    )

                return redirect('purchase_history')

        except Exception as e:
            return render(request, "purchase/new_purchase.html", {'vendors': Vendor.objects.all(), 'error': str(e)})

    return render(request, "purchase/new_purchase.html", {'vendors': Vendor.objects.all(),'category':tbl_Category.objects.all(),
                                                          'sub':tbl_SubCategory.objects.all(),'settings':ShopSettings.objects.first()})
@login_required
def purchase_list(request):
    settings = ShopSettings.objects.first()
    context={
        'settings':settings
    }
    return render(request, "purchase/purchase_list.html",context)


# --- VENDORS ---

@login_required
def vendor_list(request):
    vendors = Vendor.objects.all()
    settings = ShopSettings.objects.first()
    return render(request, "vendors/vendor_list.html", {'vendors': vendors,'settings':settings})

@login_required
def add_vendor(request):
    if request.method == "POST":
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("vendor_list")
    else:
        form = VendorForm()
    return render(request, "vendors/add_vendor.html", {'form': form})

# --- INVOICES ---

@login_required
def sales_invoices(request):
    return render(request, "invoice/sales_invoice_list.html")

@login_required
def purchase_invoices(request):
    return render(request, "invoice/purchase_invoice_list.html")

@login_required
def view_sales_invoice(request, invoice_id):
    return render(request, "invoice/view_sales_invoice.html", {"invoice_id": invoice_id})

@login_required
def view_purchase_invoice(request, invoice_id):
    return render(request, "invoice/view_purchase_invoice.html", {"invoice_id": invoice_id})


# --- TAX MASTER ---

@login_required
def tax_master(request):
    return render(request, "invoice/tax_master.html")


# --- CUSTOMERS ---

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    settings = ShopSettings.objects.first()
    return render(request, "customers/customer_list.html", {'customers': customers,'settings':settings})

@login_required
def add_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("customer_list")
    else:
        settings=ShopSettings.objects.first()
        form = CustomerForm()
    return render(request, "customers/add_customer.html", {'form': form, 'settings':settings})


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


# -----SALE ORDERS-----


@login_required
def service_order_list(request):
    return render(request, "services/service_order_list.html")

@login_required
def new_service_order(request):
    return render(request, "services/new_service_order.html")

@login_required
def view_service_order(request, order_id):
    return render(request, "services/view_service_order.html")

@login_required
def edit_service_order(request, order_id):
    return render(request, "services/edit_service_order.html")

@login_required
def delete_service_order(request, order_id):
    return render(request, "services/delete_confirm.html")

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
    settings, created = ShopSettings.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ShopSettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect("shop_settings")
    else:
        settings = ShopSettings.objects.first()
        form = ShopSettingsForm(instance=settings)

    return render(request, "settings/shop_settings.html", {"form": form,'settings':settings})

@login_required()
def theme_settings(request):
    settings, created = ThemeSettings.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ThemeSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect("theme_settings")
    else:
        form = ThemeSettingsForm(instance=settings)
        settings=ShopSettings.objects.first()

    return render(request, "settings/theme_settings.html", {"form": form,'settings':settings})

@login_required
def backup_restore(request):
    settings = ShopSettings.objects.first()
    context={
        "settings":settings
    }
    return render(request, "settings/backup_restore.html")
