from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from config.settings import CACHE_ENABLED
from main.forms import ProductFormCreate, VersionForm, VersionFormSet, ModeratorsForm
from main.models import Product, Blog, Version
from main.services import get_cached_details_for_product, get_category_list


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductFormCreate
    permission_required = 'main.add_product'
    success_url = reverse_lazy('main:index')
    extra_context = {'title': 'Создать новый продукт'}

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    success_url = reverse_lazy('main:index')
    form_class = ProductFormCreate

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        if self.request.user.is_superuser or self.request.user.is_staff:
            return self.object
        if self.object.author != self.request.user:
            raise Http404

        return self.object

    def get_success_url(self):
        return reverse('main:product_view', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        ProductVersionFormSet = inlineformset_factory(Product, Version, form=VersionForm, formset=VersionFormSet,
                                                      extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductVersionFormSet(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductVersionFormSet(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']

        if form.is_valid():
            self.object = form.save()
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.prod_title)
            self.object.author = self.request.user
            new_mat.save()

            if formset.is_valid():
                formset.instance = self.object
                formset.save()
            else:
                return super().form_invalid(form)

        return super().form_valid(form)

    def test_func(self):
        first_option = self.request.user.groups.filter(name='moderator').exists()
        second_options = self.request.user.is_superuser
        if first_option:
            self.form_class = ModeratorsForm
        if second_options:
            self.form_class = ProductFormCreate
        return first_option or second_options


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    extra_context = {'title': 'ДОБРО ПОЖАЛОВАТЬ!', 'tags': 'Мы самый лучший магазин на свете!'}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        # добавил кэширование, но вроде не работает
        get_category_list()
        return queryset


class ProductDetailView(DetailView):
    model = Product
    extra_context = {'title': 'ДОБРО ПОЖАЛОВАТЬ!', 'tags': 'Мы самый лучший магазин на свете!'}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['details'] = get_cached_details_for_product(self.object.pk)
        return context_data


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'main.delete_product'
    success_url = reverse_lazy('main:index')


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
