from django.shortcuts import render
from django.views.generic import ListView, DetailView
from main.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'main/index.html'
    extra_context = {'title': 'ДОБРО ПОЖАЛОВАТЬ!', 'tags': 'Мы самый лучший магазин на свете!'}


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product.html'
    extra_context = {'title': 'ДОБРО ПОЖАЛОВАТЬ!', 'tags': 'Мы самый лучший магазин на свете!'}


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
