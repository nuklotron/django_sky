from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

from config import settings

# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    category = models.CharField(max_length=100, verbose_name='категория')
    description = models.TextField(verbose_name='описание', **NULLABLE)

    def __str__(self):
        return f'{self.category}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    prod_title = models.CharField(max_length=100, verbose_name='наименование товара')
    prod_description = models.TextField(verbose_name='описание', **NULLABLE)
    preview_image = models.ImageField(upload_to='prev_image/', verbose_name='изображение (превью)', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.IntegerField(verbose_name='цена за покупку')
    creation_date = models.DateField(verbose_name='дата создания', auto_now=True)
    last_update = models.DateField(verbose_name='дата последнего изменения', auto_now_add=True)
    view_count = models.IntegerField(default=0, verbose_name='просмотры')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='автор', **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='опубликовать')

    def __str__(self):
        return f'{self.prod_title} - {self.category}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        permissions = [
            ('change_prod_description', 'изм.описание'),
            ('set_is_published', 'снять с публикации'),
            ('change_category_id', 'изм. категорию')
                       ]


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    slug = models.CharField(max_length=100, verbose_name='slug')
    content = models.TextField(verbose_name='содержимое', **NULLABLE)
    preview_image = models.ImageField(upload_to='content_image/', default='content_image/default.jpg', verbose_name='изображение (превью)', **NULLABLE)
    creation_date = models.DateField(verbose_name='дата создания', auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    view_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'


class Version(models.Model):
    prod_title = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='продукт', related_name='product_ver')
    version_num = models.IntegerField(default=0, verbose_name='номер версии')
    version_title = models.CharField(max_length=150, verbose_name='название версии')
    is_active = models.BooleanField(default=False, verbose_name='признак текущей версии')

    def __str__(self):
        return f'{self.version_num} ({self.version_title})'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
