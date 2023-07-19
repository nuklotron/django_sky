from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from config import settings
from main.models import Product, Blog


class ProductListView(ListView):
    model = Product
    template_name = 'main/index.html'
    extra_context = {'title': 'ДОБРО ПОЖАЛОВАТЬ!', 'tags': 'Мы самый лучший магазин на свете!'}


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product.html'
    extra_context = {'title': 'ДОБРО ПОЖАЛОВАТЬ!', 'tags': 'Мы самый лучший магазин на свете!'}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'content', 'preview_image', 'is_published',)
    success_url = reverse_lazy('main:list')
    extra_context = {'title': 'Написать статью'}

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'preview_image',)
    success_url = reverse_lazy('main:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:view', args=[self.kwargs.get('pk')])


class BlogListView(ListView):
    model = Blog
    extra_context = {'title': 'БЛОГОВАЯ ЧАСТЬ САЙТА', 'tags': 'Здесь собраны самые лучшие вымышленные статьи с помощью ChatGPT!'}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog
    extra_context = {'title': 'БЛОГОВАЯ ЧАСТЬ САЙТА', 'tags': 'Здесь собраны самые лучшие вымышленные статьи с помощью ChatGPT!'}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        if self.object.view_count == 100:
            send_mail(
                subject='Письмо от Django',
                message='Ваш пост набрал 100 просмотров',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.RECIPIENT_ADDRESS]
            )
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('main:list')


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


def toggle_activity(request, pk):
    blog_activity = get_object_or_404(Blog, pk=pk)
    if blog_activity.is_published:
        blog_activity.is_published = False
    else:
        blog_activity.is_published = True

    blog_activity.save()

    return redirect(reverse('main:list'))


def send_message():
    send_mail(
        subject='Письмо от Django',
        message='Ваш пост набрал 100 просмотров',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.RECIPIENT_ADDRESS]
    )
