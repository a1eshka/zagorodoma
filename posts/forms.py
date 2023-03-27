from django import forms
from .models import Post_sale, HouseAdditional, Rent_amenities, Cottvill


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
        fields = ['status', 'type_object','adress','body', 'year_of_construction', 'house_material' ,'square', 'floors', 'water', 'ceiling_height', 'land_area', 'land_status', 'heating', 'price', 'rent_price' ,'phone', 'houseAdditional', 'rent_amenities', 'district', 'all_images', 'urgent_sales' ]
        widgets = {
            'type_object': forms.RadioSelect(attrs={'class': 'payment-methods'}),
            'all_images':forms.FileInput(attrs={'multiple': 'multiple'}),
            'adress':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес участка'}),
            'status': forms.RadioSelect(attrs={'class': 'payment-methods'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'year_of_construction': forms.TextInput(attrs={'class': 'form-control','placeholder': '2021', 'maxlength':'5'}),
            'house_material': forms.Select(attrs={'class': 'form-control'}),
            'ceiling_height':forms.TextInput(attrs={'class': 'form-control','placeholder': '2.7 м.', 'maxlength':'3'}),
            'square': forms.TextInput(attrs={'class': 'form-control','placeholder': '120 м2', 'maxlength':'5'}),
            'floors': forms.TextInput(attrs={'class': 'form-control','placeholder': '3', 'maxlength':'2'}),
            'water': forms.Select(attrs={'class': 'form-control'}),
            'land_area': forms.TextInput(attrs={'class': 'form-control','placeholder': '8 сот.', 'maxlength':'6'}),
            'land_status': forms.Select(attrs={'class': 'form-control'}),
            'heating': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10 000 000 руб.', 'maxlength':'10'}),
            'rent_price': forms.TextInput(attrs={'class': 'form-control','maxlength':'6'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            


        }


class VillageForm(forms.ModelForm):

    class Meta:
        model = Cottvill
        exclude = ['author']
        fields = ['title', 'developer','url','adress', 'status_land', 'col_area' ,'min_area', 'max_area', 'price_area', 'сommunications', 'body', 'house_price_min', 'house_price_max', 'col_house', 'payment', 'img' ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'КП Иваново'}),
            'developer':forms.TextInput(attrs={'class': 'form-control'}),
            'url':forms.TextInput(attrs={'class': 'form-control','placeholder': 'https://www.poselok.ru'}),
            'adress': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ленинградская обл., Ломонсоовский район...'}),
            'status_land': forms.Select(attrs={'class': 'form-control', 'rows': 5}),
            'col_area': forms.TextInput(attrs={'class': 'form-control','placeholder': '56', 'maxlength':'4'}),
            'min_area': forms.TextInput(attrs={'class': 'form-control','placeholder': '6 сот.', 'maxlength':'6'}),
            'max_area':forms.TextInput(attrs={'class': 'form-control','placeholder': '24 сот.', 'maxlength':'6'}),
            'price_area': forms.TextInput(attrs={'class': 'form-control', 'maxlength':'15'}),
            'сommunications': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'house_price_min': forms.TextInput(attrs={'class': 'form-control'}),
            'house_price_max': forms.TextInput(attrs={'class': 'form-control'}),
            'col_house': forms.TextInput(attrs={'class': 'form-control'}),
            'payment':forms.TextInput(attrs={'class': 'form-control'}),
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
