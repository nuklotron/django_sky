# Generated by Django 4.2.3 on 2023-07-19 00:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_product_view_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='preview_image',
            field=models.ImageField(blank=True, default='static/default.jpg', null=True, upload_to='content_image/', verbose_name='изображение (превью)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category', verbose_name='категория'),
        ),
    ]
