from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class ShopSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    theme_color = models.CharField(max_length=7, default='#0d6efd')



class ThemeSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    font_family = models.CharField(max_length=100, choices=[
        ('Poppins', 'Poppins'),
        ('Roboto', 'Roboto'),
        ('Open Sans', 'Open Sans'),
        ('Lato', 'Lato'),
    ], default='Poppins')

    layout_mode = models.CharField(max_length=20, choices=[
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('boxed', 'Boxed'),
    ], default='light')

    sidebar_style = models.CharField(max_length=20, choices=[
        ('default', 'Default'),
        ('mini', 'Mini Sidebar'),
        ('floating', 'Floating'),
    ], default='default')

    button_style = models.CharField(max_length=20, choices=[
        ('rounded', 'Rounded'),
        ('flat', 'Flat'),
        ('outline', 'Outline'),
    ], default='rounded')

    def __str__(self):
        return f"{self.user.username}'s Theme"


class tbl_Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class tbl_SubCategory(models.Model):
    category = models.ForeignKey(tbl_Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, null=True, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class tbl_Product(models.Model):
    subcategory = models.ForeignKey(tbl_SubCategory, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    gst_number = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100)
    purchase_date = models.DateField()
    payment_mode = models.CharField(max_length=50, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('UPI', 'UPI'), ('Bank Transfer', 'Bank Transfer')])
    payment_status = models.CharField(max_length=50, choices=[('Paid', 'Paid'), ('Pending', 'Pending')])
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey('tbl_Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2)


class Sale(models.Model):
    customer_name = models.ForeignKey(Customer,on_delete=models.CASCADE)
    sale_date = models.DateField(auto_now_add=True)
    payment_mode = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(tbl_Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    designation = models.CharField(max_length=100)
    date_joined = models.DateField()
    photo = models.ImageField(upload_to="employee_photos/", null=True, blank=True)
    status = models.CharField(max_length=10, choices=[("Active", "Active"), ("Inactive", "Inactive")])

    def __str__(self):
        return self.name


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[("Present", "Present"), ("Absent", "Absent"), ("Leave", "Leave")])

    def __str__(self):
        return f"{self.employee.name} - {self.date}"


class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_date = models.DateField()
    reason = models.TextField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee.name} - {self.leave_date}"

class Expense(models.Model):
    EXPENSE_CATEGORIES = [
        ('rent', 'Rent'),
        ('salary', 'Salaries'),
        ('inventory', 'Inventory'),
        ('utilities', 'Utilities'),
        ('marketing', 'Marketing'),
        ('transport', 'Transport'),
        ('misc', 'Miscellaneous'),
    ]

    PAYMENT_MODES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('bank', 'Bank Transfer'),
    ]

    category = models.CharField(max_length=100, choices=EXPENSE_CATEGORIES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_MODES)
    reference_number = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class TailoringOrder(models.Model):
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    order_date = models.DateField()
    delivery_date = models.DateField()
    item_type = models.CharField(max_length=100)
    fabric_provided = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ])
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer_name} - {self.item_type}"


class Measurement(models.Model):
    order = models.ForeignKey(TailoringOrder, on_delete=models.CASCADE)
    body_part = models.CharField(max_length=100)
    size = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.order.customer_name} - {self.body_part}"