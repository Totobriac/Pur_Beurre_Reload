from django.contrib import admin

# Register your models here.
from .models import Product, SavedProduct


class ProductAdmin(admin.ModelAdmin):

    list_display = ('id','real_name', 'real_brand','off_id')
    search_fields = ['id']


class SavedProductAdmin(admin.ModelAdmin):

    list_display = ('id', 'username', 'sub_product', 'original_product')
    search_fields = ['username']


admin.site.register(Product, ProductAdmin)

admin.site.register(SavedProduct, SavedProductAdmin)