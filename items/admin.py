from django.contrib import admin
from .models import CustomUser, Category, Product, Personal
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Personal)