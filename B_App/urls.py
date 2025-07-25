from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("dashboard/", dashboard, name="dashboard"),

    # Products & Inventory
    path("products/", product_list, name="products"),
    path("products/add/", add_product, name="add_product"),
    path("products/stock/", stock_management, name="stock"),

    # Sales & Billing
    path("sales/new/", new_sale, name="new_sale"),
    path("sales/history/", sales_history, name="sales_history"),
    path("sales/gst-invoices/", gst_invoices, name="gst_invoices"),

    # Customers
    path("customers/", customer_list, name="customers"),

    # Tailoring Orders
    path("orders/", order_list, name="orders"),
    path("orders/new/", new_order, name="new_order"),
    path("orders/measurements/", measurement_list, name="measurements"),

    # Employees
    path("employees/", employee_list, name="employees"),
    path("employees/attendance/", attendance, name="attendance"),
    path("employees/leaves/", leaves, name="leaves"),

    # Expenses
    path("expenses/", expense_list, name="expenses"),

    # Reports
    path("reports/sales/", sales_report, name="sales_report"),
    path("reports/inventory/", inventory_report, name="inventory_report"),
    path("reports/profit/", profit_report, name="profit_report"),

    # Settings
    path("settings/shop/", shop_settings, name="shop_settings"),
    path("settings/theme/", theme_settings, name="theme_settings"),
    path("settings/backup/", backup_restore, name="backup_restore"),

    # Auth
    path("logout/", logout_view, name="logout"),
]
