from django import forms
from .models import *

from django.forms import modelformset_factory

class ShopSettingsForm(forms.ModelForm):
    class Meta:
        model = ShopSettings
        fields = ['shop_name', 'address', 'email', 'phone', 'logo', 'theme_color']
        widgets = {
            'shop_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'theme_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
        }
class ThemeSettingsForm(forms.ModelForm):
    class Meta:
        model = ThemeSettings
        fields = ['font_family', 'layout_mode', 'sidebar_style', 'button_style']
        widgets = {
            'font_family': forms.Select(attrs={'class': 'form-control'}),
            'layout_mode': forms.Select(attrs={'class': 'form-control'}),
            'sidebar_style': forms.Select(attrs={'class': 'form-control'}),
            'button_style': forms.Select(attrs={'class': 'form-control'}),
        }

class ProductCategoriesForm(forms.ModelForm):
    class Meta:
        model=tbl_Category
        fields=['name','status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model=tbl_SubCategory
        fields=['category','name','status']
        widgets={
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subcategory name'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = tbl_Product
        fields = ['subcategory', 'name', 'description', 'price', 'stock', 'image', 'status']
        widgets = {
            'subcategory': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'email', 'phone', 'address', 'company_name', 'gst_number']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control'}),

        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),

        }

