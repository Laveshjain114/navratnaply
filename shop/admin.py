from django.contrib import admin

# Register your models here.
from .models import Category, Product, Inquiry, Brand

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Inquiry)
admin.site.register(Brand)