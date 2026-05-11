from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Book, Comment


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        # fields = '__all__'
        # fields = ['name', 'text', 'price', 'published_year', 'image', 'category', 'published']
        exclude = ['views']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Nomi',
                'class': 'form-control',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'published_year': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'published': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
        }
        labels = {
            'name': 'Nomi',
            'text': 'Matni',
            'price': 'Narxi',
            'published_year': 'Yili',
            'image': 'Rasmi',
            'category': 'Kategoriyasi',
            'published': 'Saytga chiqarish'
        }

    def clean_price(self):
        errors = []
        price = self.cleaned_data.get('price')
        if price < 0:
            errors.append("Narx manfiy bo'lmasligi kerak +!!!")

        if price < 0:
            errors.append("Nimadir error")

        if errors:
            raise ValidationError(errors)

        return price

    def clean_published_year(self):
        published_year = self.cleaned_data.get('published_year')
        current_year = datetime.now().year
        if published_year > current_year:
            raise ValidationError('Kelajakda hozzircha bunday kitob chiqarilmagan😉')
        return published_year



    # def clean(self):
    #     cleaned_data = super().clean()
    #     errors = []
    #     price = cleaned_data.get("price")
    #     if price < 0:
    #         errors.append("Narx manfiy bo'lmasligi kerak!!!")
    #
    #     current_year = datetime.now().year
    #
    #     published_year = cleaned_data.get('published_year')
    #     if published_year > current_year:
    #         errors.append("Kelajakda hozzircha bunday kitob chiqarilmagan😉")
    #
    #     if errors:
    #         raise ValidationError(errors)
    #
    #     return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control ',
                'rows': 2,
                'id': 'myTextarea'
            })
        }