from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Personal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  default=None)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True,blank=True, null=True)
    profile = models.ImageField(upload_to='images/', blank=True, null=True)    

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    # Other product-related fields

    def __str__(self):
        return self.title
