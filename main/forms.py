from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

from main.models import Product, Version


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():

            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-basic'
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs['class'] = 'form-control datepicker'
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-time'
            elif isinstance(field.widget, forms.widgets.SelectMultiple):
                field.widget.attrs['class'] = 'form-control select2 select2-multiple'
            elif isinstance(field.widget, forms.widgets.Select):
                field.widget.attrs['class'] = 'form-control select2'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductFormCreate(StyleFormMixin, forms.ModelForm):

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


class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'


class VersionFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()
        active_list = [form.cleaned_data['is_active'] for form in self.forms if 'is_active' in form.cleaned_data]
        if active_list.count(True) > 1:
            raise forms.ValidationError('Активная версия может быть только одна!')

