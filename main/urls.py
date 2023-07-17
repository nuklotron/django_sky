from django.urls import path

from main.apps import MainConfig
from main.views import contacts, ProductDetailView, ProductListView


app_name = MainConfig.name


urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contacts/', contacts, name='contacts'),
    path('<int:pk>/product/', ProductDetailView.as_view(), name='product'),
]
