from django.urls import path

from main.apps import MainConfig
from main.views import index, contacts, product


app_name = MainConfig.name


urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('product/', product, name='product'),
]

