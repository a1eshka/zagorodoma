from django import forms
from django.forms import CheckboxSelectMultiple,ClearableFileInput
from .models import Post_sale,Status, Land_status, Heating, House_material, Water, HouseAdditional, Rent_amenities


class PostForm(forms.ModelForm):

    all_images = forms.ImageField(label=u'Фотографии', widget=forms.FileInput(attrs={'multiple': 'multiple'}))
    houseAdditional = forms.ModelMultipleChoiceField(
        label='Благоустройтво',
        widget=forms.CheckboxSelectMultiple, 
        queryset=HouseAdditional.objects.all(),
        required=False, 
        )
    rent_amenities = forms.ModelMultipleChoiceField(
        label='Удобства',
        widget=forms.CheckboxSelectMultiple, 
        queryset=Rent_amenities.objects.all(),
        required=False, 
        )

    class Meta:
        model = Post_sale
        exclude = ['author']
        fields = ['status', 'type_object','adress','body', 'year_of_construction', 'house_material' ,'square', 'floors', 'water', 'ceiling_height', 'land_area', 'land_status', 'heating', 'price', 'rent_price' ,'phone', 'houseAdditional', 'rent_amenities', 'all_images' ]
        widgets = {
            'type_object': forms.Select(attrs={'class': 'form-control'}),
            'all_images':forms.FileInput(attrs={'multiple': 'multiple'}),
            'adress':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес участка'}),
            'status': forms.RadioSelect(attrs={'class': 'payment-methods'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'year_of_construction': forms.TextInput(attrs={'class': 'form-control'}),
            'house_material': forms.Select(attrs={'class': 'form-control'}),
            'ceiling_height':forms.TextInput(attrs={'class': 'form-control'}),
            'square': forms.TextInput(attrs={'class': 'form-control'}),
            'floors': forms.TextInput(attrs={'class': 'form-control'}),
            'water': forms.Select(attrs={'class': 'form-control'}),
            'land_area': forms.TextInput(attrs={'class': 'form-control'}),
            'land_status': forms.Select(attrs={'class': 'form-control'}),
            'heating': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'rent_price': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),


        }
  
    #title = forms.CharField(max_length=200, label='Заголовок')
    #status = forms.ModelChoiceField(empty_label='Не выбрано', queryset=Status.objects.all(), label='Тип сделки')
    #body = forms.CharField(label='Описание')
    #square = forms.CharField(max_length=4, label='Площадь дома')
    #floors = forms.CharField(max_length=2, label='Этажей в доме')
    #land_area = forms.CharField(max_length=7, label='Площадь участка')
    #land_status = forms.ModelChoiceField(empty_label='Не выбрано',  queryset=Land_status.objects.all(), label='Статус земли')
    #heating = forms.ModelChoiceField(empty_label='Не выбрано', queryset=Heating.objects.all(), label='Отопление')
    #year_of_construction = forms.CharField(max_length=4, label='Год постройки')
    #house_material = forms.ModelChoiceField(empty_label='Не выбрано', queryset=House_material.objects.all(), label='Материал Дома')
    #price = forms.CharField(max_length=30, label='Цена')
