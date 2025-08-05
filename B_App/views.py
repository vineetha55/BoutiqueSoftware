from django.contrib import messages
from django.core.management import call_command
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
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
    settings = ShopSettings.objects.first()
    products = tbl_Product.objects.all()
    return render(request, "products/stock.html", {
        "products": products,
        "settings": settings
    })
@login_required
def update_stock(request, pk):
    product = tbl_Product.objects.get(pk=pk)
    settings = ShopSettings.objects.first()

    if request.method == "POST":
        new_stock = request.POST.get("stock")
        if new_stock.isdigit():
            product.stock = int(new_stock)
            product.save()
            return redirect("stock")
        else:
            return render(request, "products/update_stock.html", {
                "product": product,
                "error": "Please enter a valid number",
                "settings": settings
            })

    return render(request, "products/update_stock.html", {
        "product": product,
        "settings": settings
    })

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
    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        contact = request.POST.get("contact")
        payment_mode = request.POST.get("payment_mode")
        payment_status = request.POST.get("payment_status")
        notes = request.POST.get("notes")
        total_items = int(request.POST.get("total_items"))

        sale = Sale.objects.create(
            customer_name=customer_name,
            contact=contact,
            payment_mode=payment_mode,
            payment_status=payment_status,
            notes=notes,
            created_by=request.user
        )

        for i in range(1, total_items + 1):
            product_id = request.POST.get(f"product_{i}")
            qty = request.POST.get(f"quantity_{i}")
            price = request.POST.get(f"price_{i}")
            gst = request.POST.get(f"gst_{i}")

            if product_id and qty:
                SaleItem.objects.create(
                    sale=sale,
                    product_id=product_id,
                    quantity=qty,
                    unit_price=price,
                    gst_percentage=gst or 0
                )

        return redirect("sales_history")

    products = tbl_Product.objects.all()
    settings=ShopSettings.objects.first()
    customer=Customer.objects.all()
    return render(request, "sales/new_sale.html", {"products": products,"settings":settings,"customer":customer})


@login_required
def sales_history(request):
    sales = Sale.objects.all().order_by("-sale_date")
    settings = ShopSettings.objects.first()
    return render(request, "sales/sales_history.html", {"sales": sales,"settings":settings})


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
                                                          'sub':tbl_SubCategory.objects.all(),'settings':ShopSettings.objects.first(),
                                                          "products":tbl_Product.objects.all()})
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
        settings = ShopSettings.objects.first()
    return render(request, "vendors/add_vendor.html", {'form': form,"settings":settings})

# --- INVOICES ---

@login_required
def sales_invoices(request):
    sales = Sale.objects.all().order_by('-sale_date')
    settings = ShopSettings.objects.first()
    return render(request, "invoices/sales_invoices.html", {'sales': sales,"settings":settings})

@login_required
def purchase_invoices(request):
    purchases = Purchase.objects.all().order_by('-purchase_date')
    settings = ShopSettings.objects.first()
    return render(request, "invoices/purchase_invoices.html", {'purchases': purchases,"settings":settings})

@login_required
def view_purchase_invoice(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    items = PurchaseItem.objects.filter(purchase=purchase)
    settings = ShopSettings.objects.first()
    return render(request, "invoices/view_purchase_invoice.html", {
        'purchase': purchase,
        'items': items,
        "settings":settings
    })

@login_required
def view_sales_invoice(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    items = SaleItem.objects.filter(sale=sale)
    settings = ShopSettings.objects.first()
    return render(request, "invoices/view_sales_invoice.html", {
        'sale': sale,
        'items': items,
        'settings':settings
    })

# --- TAX MASTER ---

@login_required
def tax_master(request):
    settings = ShopSettings.objects.first()
    return render(request, "invoices/tax_master.html",{"settings":settings})


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
    orders = TailoringOrder.objects.all()
    settings = ShopSettings.objects.first()
    return render(request, "orders/order_list.html", {"orders": orders,"settings":settings})

@login_required
def new_order(request):
    if request.method == "POST":
        TailoringOrder.objects.create(
            customer_name=request.POST["customer_name"],
            phone=request.POST["phone"],
            order_date=request.POST["order_date"],
            delivery_date=request.POST["delivery_date"],
            item_type=request.POST["item_type"],
            fabric_provided=request.POST.get("fabric_provided") == "on",
            status=request.POST["status"],
            notes=request.POST.get("notes"),
        )
        return redirect("orders")
    settings=ShopSettings.objects.first()

    return render(request, "orders/new_order.html",{"settings":settings})


@login_required
def measurement_list(request):
    measurements = Measurement.objects.select_related("order")
    settings = ShopSettings.objects.first()
    return render(request, "orders/measurement_list.html", {"measurements": measurements,"settings":settings})


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
def add_employee(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        designation = request.POST.get("designation")
        date_joined = request.POST.get("date_joined")
        status = request.POST.get("status")
        photo = request.FILES.get("photo")

        Employee.objects.create(
            name=name, email=email, phone=phone, designation=designation,
            date_joined=date_joined, status=status, photo=photo
        )
        messages.success(request, "Employee added successfully.")
        return redirect('employees')
    settings=ShopSettings.objects.first()
    return render(request, "employees/add_employee.html",{"settings":settings})
@login_required
def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == "POST":
        employee.name = request.POST.get("name")
        employee.email = request.POST.get("email")
        employee.phone = request.POST.get("phone")
        employee.designation = request.POST.get("designation")
        employee.date_joined = request.POST.get("date_joined")
        employee.status = request.POST.get("status")
        if request.FILES.get("photo"):
            employee.photo = request.FILES.get("photo")
        employee.save()
        messages.success(request, "Employee updated successfully.")
        return redirect('employees')
    settings = ShopSettings.objects.first()
    return render(request, "employees/edit_employee.html", {'employee': employee,"settings":settings})


@login_required
def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    messages.success(request, "Employee deleted successfully.")
    return redirect('employees')

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    settings = ShopSettings.objects.first()
    return render(request, "employees/employee_list.html", {'employees': employees,"settings":settings})


@login_required
def attendance(request):
    settings = ShopSettings.objects.first()
    attendance_records = Attendance.objects.select_related('employee').order_by('-date')
    return render(request, "employees/attendance.html", {'attendance_records': attendance_records,"settings":settings})


@login_required
def leaves(request):
    settings = ShopSettings.objects.first()
    leave_records = Leave.objects.select_related('employee').order_by('-leave_date')
    return render(request, "employees/leaves.html", {'leave_records': leave_records,"settings":settings})


# --- EXPENSES ---

@login_required
def expense_list(request):
    expenses = Expense.objects.all().order_by("-date")
    settings = ShopSettings.objects.first()
    return render(request, "expenses/expense_list.html", {"expenses": expenses,"settings":settings})


@login_required
def add_expense(request):
    if request.method == "POST":
        category = request.POST.get("category")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        description = request.POST.get("description")

        Expense.objects.create(
            category=category,
            amount=amount,
            date=date,
            description=description,
            added_by=request.user
        )
        messages.success(request, "Expense added successfully.")
        return redirect("expenses")
    settings = ShopSettings.objects.first()
    return render(request, "expenses/add_expense.html",{"settings":settings})
# --- REPORTS ---

@login_required
def sales_report(request):
    sales = Sale.objects.all().order_by("-sale_date")
    settings=ShopSettings.objects.first()
    return render(request, "reports/sales_report.html", {"sales": sales,"settings":settings})

@login_required
def inventory_report(request):
    products = tbl_Product.objects.all()
    settings = ShopSettings.objects.first()
    return render(request, "reports/inventory_report.html", {"products": products,"settings":settings})

@login_required
def profit_report(request):
    sales = Sale.objects.all()
    purchases = Purchase.objects.all()
    settings = ShopSettings.objects.first()
    return render(request, "reports/profit_report.html", {
        "sales": sales,
        "purchases": purchases,
        "settings":settings
    })
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
import os
import io
@login_required
def backup_restore(request):
    settings = ShopSettings.objects.first()
    return render(request, "settings/backup_restore.html", {"settings": settings})

@login_required
def backup_download(request):
    buffer = io.StringIO()
    call_command('dumpdata', format='json', indent=2, stdout=buffer)
    response = HttpResponse(buffer.getvalue(), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=backup.json'
    return response

@login_required
def backup_upload(request):
    if request.method == "POST" and request.FILES.get("backup_file"):
        file = request.FILES["backup_file"]
        try:
            file_data = file.read().decode("utf-8")
            buffer = io.StringIO(file_data)
            call_command('loaddata', buffer)
            messages.success(request, "Data restored successfully.")
        except Exception as e:
            messages.error(request, f"Failed to restore: {str(e)}")
        return redirect('backup_restore')