import json

from django.core.management import BaseCommand
from main.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        category_for_create = []
        with open('data.json', 'r', encoding='UTF8') as data:
            data = json.loads(data.read())
            for cat_item in data:
                category_for_create.append(
                    Category(**cat_item['fields'])
                )

        Category.objects.bulk_create(category_for_create)
