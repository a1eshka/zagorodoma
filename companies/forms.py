from django import forms
from .models import Constcomp, Services


class ConstcompForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        label='Услуги',
        widget=forms.CheckboxSelectMultiple, 
        queryset=Services.objects.all(),
        required=False, 
        )
    class Meta:
        model = Constcomp
        exclude = ['author']
        fields = ['title', 'youtube', 'url', 'adress', 'services', 'body', 'phone', 'img']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'СК Загородома'}),
            'youtube':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'https://www.youtube.com/channel/...'}),
            'url':forms.TextInput(attrs={'class': 'form-control','placeholder': 'https://www.skstroi.ru'}),
            'adress': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ленинградская обл., Ломонсоовский район...'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder':'Опишите Вашу строительную компанию.'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),     
        }