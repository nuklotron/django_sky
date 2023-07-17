from django.shortcuts import render

# Create your views here.
from main.models import Product


def index(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list,
        'title': 'ДОБРО ПОЖАЛОВАТЬ!',
        'tags': 'Мы самый лучший магазин на свете!'
    }
    return render(request, 'main/index.html', context)


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


def product(request, pk):
    product_item = Product.objects.get(pk=pk)
    print(product_item)
    context = {
        'object_list': product_item,
        'title': f'{product_item.prod_title}',
        'tags': f'{product_item.prod_description} - {product_item.price} руб.'
    }

    return render(request, 'main/product.html', context)
