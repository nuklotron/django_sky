from django import forms

from main.models import Product, Version


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):

    PROHIBITED = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ('prod_title', 'prod_description', 'preview_image', 'category', 'price',)

    def clean_prod_title(self):
        cleaned_data = self.cleaned_data.get('prod_title').lower()

        data_split = cleaned_data.split()

        for word in data_split:
            if word in self.PROHIBITED:
                raise forms.ValidationError('Недопустимое название')

        return cleaned_data


class VersionFrom(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'

    def clean_prod_title(self):
        cleaned_data = self.cleaned_data.get('is_active')
        if cleaned_data:
            raise forms.ValidationError('Активная версия может быть только одна!')

        return cleaned_data
