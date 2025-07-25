from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class ShopSettings(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    theme_color = models.CharField(max_length=7, default='#0d6efd')  # Hex color