from django.db import models

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

    def __str__(self):
        return f'{self.prod_title} - {self.price} руб. - {self.category}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
