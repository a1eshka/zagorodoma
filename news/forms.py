from django import forms
from .models import News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = ['author']
        fields = ['title', 'body', 'img', 'published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название новости'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Текст новости' }),  
        }