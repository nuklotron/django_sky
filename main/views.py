from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView, DetailView

from main.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'main/index.html'
    # title = 'ДОБРО ПОЖАЛОВАТЬ!'
    # tags = 'Мы самый лучший магазин на свете!'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product.html'


def contacts(request):

    if request == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"{name} ({phone}) - {message}")

    context = {
        'title': 'Контакты',
        'tags': 'Для связи с нами, заполните форму ниже'
    }

    return render(request, 'main/contacts.html', context)


# def product(request, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#     context = {
#         'object_list': product_item,
#         'title': f'{product_item.prod_title}',
#         'tags': f'{product_item.prod_description}',
#     }
#
#     return render(request, 'main/product.html', context)
