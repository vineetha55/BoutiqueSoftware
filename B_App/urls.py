from django.urls import path
from .views import *

urlpatterns = [
    # Auth & Dashboard
    path("", index, name="index"),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", logout_view, name="logout"),

    # Product Management
    path("products/", product_list, name="products"),
    path("products/add/", add_product, name="add_product"),
    path("products/stock/", stock_management, name="stock"),
    path("products/categories/", product_categories, name="product_categories"),
    path("products/sub_categories/",sub_categories,name="sub_categories"),
    path("category/add/",category_add,name="category_add"),
    path("subcategory/add/",subcategory_add,name="subcategory_add"),
    path("products/stock/update/<int:pk>/", update_stock, name="update_stock"),

    # Sales
    path("sales/new/", new_sale, name="new_sale"),
    path("sales/history/", sales_history, name="sales_history"),
    path('get-product/<int:product_id>/', get_product_data, name='get_product_data'),
    path('customers/ajax/add/', add_customer_ajax, name='add_customer_ajax'),
    path('sale/<int:sale_id>/', sale_detail, name='sale_detail'),


    # Purchases
    path("purchase/new/", new_purchase, name="new_purchase"),
    path("purchase/history/", purchase_list, name="purchase_list"),
    path("get-product/<int:product_id>/", get_product_details, name="get_product"),



    # Vendors
    path("vendors/", vendor_list, name="vendor_list"),
    path("vendors/add/", add_vendor, name="add_vendor"),

    # Invoices
    path("invoices/sales/", sales_invoices, name="sales_invoices"),
    path("invoices/purchase/", purchase_invoices, name="purchase_invoices"),
    path("invoices/sales/<int:invoice_id>/", view_sales_invoice, name="view_sales_invoice"),
    path("invoices/purchase/<int:invoice_id>/", view_purchase_invoice, name="view_purchase_invoice"),

    # Tax Master
    path("tax-master/", tax_master, name="tax_master"),

    # Customers
    path("customers/", customer_list, name="customers"),
    path("customers/add/", add_customer, name="add_customer"),

    # Tailoring Orders
    path("orders/", order_list, name="orders"),
    path("orders/new/", new_order, name="new_order"),
    path("orders/measurements/", measurement_list, name="measurements"),

    #service orders
    path("services/new/", new_service_order, name="new_service_order"),
    path("services/", service_order_list, name="service_order_list"),
    path("services/<int:order_id>/view/", view_service_order, name="view_service_order"),
    path("services/<int:order_id>/edit/", edit_service_order, name="edit_service_order"),
    path("services/<int:order_id>/delete/", delete_service_order, name="delete_service_order"),

    # Employees
    path("employees/", employee_list, name="employees"),
    path("employees/attendance/", attendance, name="attendance"),
    path("employees/leaves/", leaves, name="leaves"),
    path("employees/add/", add_employee, name="add_employee"),
    path("employees/edit/<int:id>/", edit_employee, name="edit_employee"),
    path("employees/delete/<int:id>/", delete_employee, name="delete_employee"),

    # Expenses
    path("expenses/", expense_list, name="expenses"),
    path("expenses/add/", add_expense, name="add_expense"),

    # Reports
    path("reports/sales/", sales_report, name="sales_report"),
    path("reports/inventory/", inventory_report, name="inventory_report"),
    path("reports/profit/", profit_report, name="profit_report"),

    # Settings
    path("settings/shop/", shop_settings, name="shop_settings"),
    path("settings/theme/", theme_settings, name="theme_settings"),
    path("settings/backup/", backup_restore, name="backup_restore"),
    path("settings/backup/download/", backup_download, name="backup_download"),
    path("settings/backup/upload/", backup_upload, name="backup_upload"),
]
