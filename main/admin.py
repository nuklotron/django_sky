from django.contrib import admin

# Register your models here.
from main.models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'prod_title', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('prod_title', 'description',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category')
    list_filter = ('category',)
    search_fields = ('category',)
