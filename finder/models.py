from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=2000)    
    brand = models.CharField(max_length=2000)
    nutrition_grade = models.CharField(max_length=10)
    picture = models.URLField(max_length=2000)
    off_id = models.BigIntegerField()
    categories = models.TextField(max_length=5000)
    fat = models.FloatField(max_length=100)
    satured_fat = models.FloatField(max_length=100)
    sugars = models.FloatField(max_length=100)
    salt = models.FloatField(max_length=100)
    real_name = models.CharField(max_length=2000)
    real_brand = models.CharField(max_length=2000)


class SavedProduct(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    sub_product = models.ForeignKey(Product, related_name='savedproducts', on_delete=models.CASCADE, null=True)
    original_product = models.ForeignKey(Product, related_name='original_products', on_delete=models.CASCADE, null=True)
