from django.conf import settings
from django.core.cache import cache

from main.models import Product, Category


def get_cached_details_for_product(product_pk):
    if settings.CACHE_ENABLED:
        key = f'details_list_{product_pk}'
        detail_list = cache.get(key)
        if detail_list is None:
            detail_list = Product.objects.filter(pk=product_pk)
            cache.set(key, detail_list)

    else:
        detail_list = Product.objects.filter(pk=product_pk)

    return detail_list


def get_category_list():
    if settings.CACHE_ENABLED:
        key = 'category_list'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.all()
            cache.set(key, category_list)
    else:
        category_list = Category.objects.all()
    return category_list
