from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from multiprocessing import context
import json
from re import template
import smtplib
from sre_constants import SUCCESS
import ssl
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views import generic
from requests import request
from companies.models import Constcomp
from news.models import News
from posts_project.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
from .models import BannerPost, Post_sale,PostImage, Subscribers, Type_object, Status, Land_status, House_material, District, Cottvill
from .forms import PostForm, SubscribeForm, VillageForm
from django.shortcuts import get_object_or_404, redirect, render
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from datetime import date
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib import messages
from django.db.models import Avg
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy



class FilterMain:
    def get_typeobjects(self):
        return Type_object.objects.all()

    def get_status(self):
        return Status.objects.all()

    def get_landstatus(self):
        return Land_status.objects.all()
    
    def get_housematerial(self):
        return House_material.objects.all()
        
    def get_district(self):
        return District.objects.all()

class SalesListView(FilterMain, generic.ListView):
    """Вывод постов со статусом Продажа"""
    model = Post_sale
    template_name = 'sales.html'
    context_object_name = 'sales'
    def get_queryset(self):
        return Post_sale.objects.filter(status='2').filter(published=True).order_by('-created_at')[:6]
    
    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского класса ListView
        context = super().get_context_data(**kwargs)
        # Дополняем контекст нужным нам значением
        context['total_data'] = Post_sale.objects.filter(status='2').filter(published=True).count()
        return context

class DomaListView(FilterMain, generic.ListView):
    """Вывод постов с типом Дом"""
    model = Post_sale
    template_name = 'doma.html'
    context_object_name = 'doma'
    paginate_by = 6
    def get_queryset(self):
        return Post_sale.objects.filter(type_object='2').filter(published=True).order_by('-created_at')[:6]
    
    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского класса ListView
        context = super().get_context_data(**kwargs)
        # Дополняем контекст нужным нам значением
        context['total_data'] = Post_sale.objects.filter(type_object='2').filter(published=True).count()
        return context

class VillageListView(generic.ListView):
    """Вывод всех поселков"""
    model = Cottvill
    template_name = 'village/village.html'
    context_object_name = 'village'

    def get_queryset(self):
        return Cottvill.objects.filter(published=True)[:6]
    
    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского класса ListView
        context = super().get_context_data(**kwargs)
        # Дополняем контекст нужным нам значением
        context['total_data'] = Cottvill.objects.filter(published=True).count()
        return context
    
   
class YchastkiListView(FilterMain, generic.ListView):
    """Вывод постов с типом Участок"""
    model = Post_sale
    template_name = 'ychastki.html'
    context_object_name = 'ychastki'
    def get_queryset(self):
        return Post_sale.objects.filter(type_object='5').filter(published=True).order_by('-created_at')[:6]
    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского класса ListView
        context = super().get_context_data(**kwargs)
        # Дополняем контекст нужным нам значением
        context['total_data'] = Post_sale.objects.filter(type_object='5').filter(published=True).count()
        return context

class RentListView(FilterMain, generic.ListView):
    """Вывод постов с типом Аренда"""
    model = Post_sale
    template_name = 'rent.html'
    context_object_name = 'rent'
    def get_queryset(self):
        return Post_sale.objects.filter(status='3').filter(published=True).order_by('-created_at')[:6]
    
    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского класса ListView
        context = super().get_context_data(**kwargs)
        # Дополняем контекст нужным нам значением
        context['total_data'] = Post_sale.objects.filter(status='3').filter(published=True).count()
        return context

class HomePageView(FilterMain, ListView):
    """Вывод всех постов на главной"""
    model = Post_sale, Cottvill, News, Constcomp
    template_name = 'home.html'
    context_object_name = 'all_posts_list'

    def get_queryset(self):
        return Post_sale.objects.filter(published=True).order_by('-created_at')[:9]


    def get_context_data(self, **kwargs):
        
        # Получаем контекст из родительского класса ListView
        context = super().get_context_data(**kwargs)
        # Дополняем контекст нужным нам значением
        context['sale_status_post'] = Post_sale.objects.filter(status=2).filter(published=True).count()
        context['rent_status_post'] = Post_sale.objects.filter(status=3).filter(published=True).count()
        context['companies_post'] = Constcomp.objects.filter(published=True).count()
        context['col_village'] = Cottvill.objects.filter(published=True).count()
        context['villages'] = Cottvill.objects.filter(main_slider=True).filter(published=True)
        context['news'] = News.objects.filter(published=True)
        context['form'] = SubscribeForm()
        context['total_data'] = Post_sale.objects.filter(published=True).count()
        context['avg_price_area'] = Post_sale.objects.filter(published=True).aggregate(Avg('price'))
        return context  

class MyPostListView(generic.ListView):
    """Вывод моих постов в личном кабинете"""
    model = Post_sale
    template_name = 'profile/my_posts.html'
    context_object_name = 'my_posts'

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['my_post'] = Post_sale.objects.filter(author=self.request.user.id)
       return context

class HomeDetailView(FilterMain, DetailView):
    """Детальная страница поста"""
    model = Post_sale,BannerPost
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post_sale.objects.all()
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['banners'] = BannerPost.objects.all()
       return context
    
    def get(self, request, *args, **kwargs):

        id = self.kwargs['pk']
        post = get_object_or_404(Post_sale, id=id)
        fav = False
        self.object = super(HomeDetailView, self).get_object()
        self.object.views += 1
        self.object.save()
        if post.favourites.filter(id=request.user.id).exists():
            fav = True
        else:
            fav = False

        context = {
            'post': post,
            'fav': fav
        }
        return render(request, 'post_detail.html', context)

class VillageDetailView(FilterMain, DetailView):
    """Детальная страница поселка"""
    model = VillageForm
    template_name = 'village/village_detail.html'
    context_object_name = 'village'

    def get(self, request, *args, **kwargs):

        id = self.kwargs['village_slug']
        village = get_object_or_404(Cottvill, slug=id)
        context = {
            'village': village,
        }


        return render(request, 'village/village_detail.html', context)

class HomeCreateView(CreateView):
    """Создание нового поста"""
    form_class = PostForm
    template_name = 'post_new.html'
    model = Post_sale

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        bound_form = self.form_class(request.POST, request.FILES)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.author = request.user
            new_obj = bound_form.save()
            messages.success(request, 'Ваше объявление успешно опубликовано.')
            post_url = request.build_absolute_uri(new_obj.get_absolute_url())
            html = '''
<html>
<body>
<table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top;background-color:#FFFFFF">
<tr>
<td valign="top" style="padding:0;Margin:0">
<table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
<tr>
<td align="center" style="padding:0;Margin:0">
<table bgcolor="#efefef" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#EFEFEF;border-radius:20px 20px 0 0;width:600px">
<tr>
<td align="left" style="padding:0;Margin:0;padding-top:40px;padding-left:40px;padding-right:40px">
<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="center" valign="top" style="padding:0;Margin:0;width:520px">
<table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="left" style="padding:0;Margin:0;font-size:0px"><a target="_blank" href="" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#2D3142;font-size:18px"><img src="https://gtbyhc.stripocdn.email/content/guids/CABINET_ee77850a5a9f3068d9355050e69c76d26d58c3ea2927fa145f0d7a894e624758/images/group_4076323.png" alt="Confirm email" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;border-radius:100px" width="100" title="Confirm email"></a></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
<tr>
<td align="left" style="padding:0;Margin:0;padding-top:20px;padding-left:40px;padding-right:40px">
<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="center" valign="top" style="padding:0;Margin:0;width:520px">
<table cellpadding="0" cellspacing="0" width="100%" bgcolor="#fafafa" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:separate;border-spacing:0px;background-color:#fafafa;border-radius:10px" role="presentation">
<tr>
<td align="left" style="padding:20px;Margin:0"><h3 style="Margin:0;line-height:34px;mso-line-height-rule:exactly;font-family:Imprima, Arial, sans-serif;font-size:28px;font-style:normal;font-weight:bold;color:#2D3142">Поздравляем!</h3><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Imprima, Arial, sans-serif;line-height:27px;color:#2D3142;font-size:18px"><br></p><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:Imprima, Arial, sans-serif;line-height:27px;color:#2D3142;font-size:18px">Ваше объявление было успешно опубликовано на нашем сайте.<br>Объявление доступно по ссылке: {}&nbsp;<br></p></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
</table>
<table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
<tr>
<td align="center" style="padding:0;Margin:0">
<table bgcolor="#efefef" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#EFEFEF;width:600px">
<tr>
<td align="left"
style="Margin:0;padding-top:30px;padding-bottom:40px;padding-left:40px;padding-right:40px">
<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="center" valign="top" style="padding:0;Margin:0;width:520px">
<table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="center" style="padding:0;Margin:0"><!--[if mso]><a href="" target="_blank" hidden>
<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" esdevVmlButton href=""
style="height:56px; v-text-anchor:middle; width:520px" arcsize="50%" stroke="f" fillcolor="#7630f3">
<w:anchorlock></w:anchorlock>
<center style='color:#ffffff; font-family:Imprima, Arial, sans-serif; font-size:22px; font-weight:700; line-height:22px; mso-text-raise:1px'>Перейти к объявлению</center>
</v:roundrect></a>
<![endif]--><!--[if !mso]><!— —><span class="msohide es-button-border" style="border-style:solid;border-color:#2CB543;background:#7630f3;border-width:0px;display:block;border-radius:30px;width:auto;mso-border-alt:10px;mso-hide:all"><a href="{}" class="es-button msohide" target="_blank" style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;color:#FFFFFF;font-size:22px;padding:15px 20px 15px 20px;display:block;background:#7630f3;border-radius:30px;font-family:Imprima, Arial, sans-serif;font-weight:bold;font-style:normal;line-height:26px;width:auto;text-align:center;mso-hide:all;padding-left:5px;padding-right:5px;border-color:#7630f3">Перейти к объявлению</a></span><!--<![endif]--></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
<tr>
<td align="left" style="padding:0;Margin:0;padding-left:40px;padding-right:40px">
<table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="center" valign="top" style="padding:0;Margin:0;width:520px">
<table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td align="left" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:-apple-system, blinkmacsystemfont, 'segoe ui', roboto, helvetica, arial, sans-serif, 'apple color emoji', 'segoe ui emoji', 'segoe ui symbol';line-height:27px;color:#2D3142;font-size:18px">С Уважением,<br>Команда Zagorodoma.</p></td>
</tr>
<tr>
<td align="center" style="padding:0;Margin:0;padding-bottom:20px;padding-top:40px;font-size:0">
<table border="0" width="100%" height="100%" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
<tr>
<td style="padding:0;Margin:0;border-bottom:1px solid #666666;background:unset;height:1px;width:100%;margin:0px"></td>
</tr>
</table></td>
</tr>
<tr>
<td align="center" style="padding:0;Margin:0;padding-top:10px;padding-bottom:10px;font-size:0px"><a target="_blank" href="https://zagorodoma.ru" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;text-decoration:underline;color:#2D3142;font-size:18px"><img class="adapt-img" src="http://cdn.zagorodoma.ru/media/static/logo-v2.png" alt="zagorodoma.ru" width="29%" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" title="zagorodoma.ru"></a></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
</table></td>
</tr>
</table>
</body>
</html>
'''.format(post_url, post_url, post_url)
            email_from = EMAIL_HOST_USER
            password = EMAIL_HOST_PASSWORD
            email_to = new_obj.author.email
            email_message = MIMEMultipart()
            email_message['From'] = DEFAULT_FROM_EMAIL
            email_message['To'] = email_to
            email_message['Subject'] = f'Ваше объявление успешно опубликовано.'
# Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
            email_message.attach(MIMEText(html, "html"))
            email_string = email_message.as_string()
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.mail.ru", 465, context=context) as server:
                server.login(email_from, password)
                server.sendmail(email_from, email_to, email_string)
            for f in request.FILES.getlist('all_images'):
                data = f.read() #Если файл целиком умещается в памяти
                photo = PostImage(post=new_obj)
                photo.image_data_link.save(f.name, ContentFile(data))
                photo.save()
            return redirect(new_obj)
        return render(request, self.template_name, context={'form': bound_form})

class VillageCreateView(CreateView):
    """Создание нового послека"""
    form_class = VillageForm
    template_name = 'village/add_village.html'
    model = Cottvill

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def image_upload_view(self, request):
        if request.method == 'POST':
            form = VillageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, self.template_name, {'form': form, 'img_obj': img_obj})
        else:
            form = VillageForm()
        return render(request, self.template_name, {'form': form})

class FilterPostsView(FilterMain, ListView):
    template_name = 'home.html'
    """Фильтрация постов на главной"""
    def get_queryset(self):
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price or max_price and 'type_object' in self.request.GET and 'status' in self.request.GET:
             queryset = Post_sale.objects.filter(
                Q(price__gte=min_price),
                Q(price__lte=max_price),
                Q(type_object__in=self.request.GET.getlist("type_object")),
                Q(status__in=self.request.GET.getlist("status")),
                )

        elif 'type_object' in self.request.GET and 'status' in self.request.GET:
            queryset = Post_sale.objects.filter(
                Q(type_object__in=self.request.GET.getlist("type_object")),
                Q(status__in=self.request.GET.getlist("status")),

                )
        else:
            queryset = Post_sale.objects.filter(
                Q(type_object__in=self.request.GET.getlist("type_object")) |
                Q(status__in=self.request.GET.getlist("status")) 

                )
        return queryset



class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""
    template_name = 'ajax/posts.html'

    def get_queryset(self):
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price or max_price and 'type_object' in self.request.GET and 'status' in self.request.GET:
            queryset = Post_sale.objects.filter(
                Q(price__gte=min_price),
                Q(price__lte=max_price),
                Q(type_object__in=self.request.GET.getlist("type_object")),
                Q(status__in=self.request.GET.getlist("status")),
                ).values()

        elif 'type_object' in self.request.GET and 'status' in self.request.GET:
            queryset = Post_sale.objects.filter(
                Q(type_object__in=self.request.GET.getlist("type_object")),
                Q(status__in=self.request.GET.getlist("status")),

                ).values()
        else:
            queryset = Post_sale.objects.filter(
                Q(type_object__in=self.request.GET.getlist("type_object")) |
                Q(status__in=self.request.GET.getlist("status")) 

                ).values()
        
        return queryset



def json_filter(request, page=1):
    status=request.GET.getlist('status[]')
    land_status=request.GET.getlist('land_status[]')
    type_objects=request.GET.getlist('type_object[]')
    house_material=request.GET.getlist('house_material[]')
    district=request.GET.getlist('district[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    minFloors = request.GET['minFloors']
    maxFloors = request.GET['maxFloors']
    minLand_area = request.GET['minLand_area']
    maxLand_area = request.GET['maxLand_area']
    maxsquare = request.GET['maxsquare']
    minsquare = request.GET['minsquare']
    allPosts=Post_sale.objects.all().filter(published=True).order_by('-created_at')
    if minLand_area:
        allPosts=allPosts.filter(land_area__gte=minLand_area)
    if maxLand_area:
        allPosts=allPosts.filter(land_area__lte=maxLand_area)
    if minPrice:
        allPosts=allPosts.filter(price__gte=minPrice)
    if maxPrice:
        allPosts=allPosts.filter(price__lte=maxPrice)
    if minsquare:
        allPosts=allPosts.filter(square__gte=minsquare)
    if maxsquare:
        allPosts=allPosts.filter(square__lte=maxsquare)
    if minFloors:
        allPosts=allPosts.filter(floors__gte=minFloors)
    if maxFloors:
        allPosts=allPosts.filter(floors__lte=maxFloors)
    if len(type_objects)>0:
        allPosts=allPosts.filter(type_object__id__in=type_objects)
    if len(status)>0:
        allPosts=allPosts.filter(status__id__in=status)
    if len(land_status)>0:
        allPosts=allPosts.filter(land_status__id__in=land_status)
    if len(house_material)>0:
        allPosts=allPosts.filter(house_material__id__in=house_material) 
    if len(district)>0:
        allPosts=allPosts.filter(district__id__in=district) 

    t=render_to_string('ajax/posts.html',{'object_list':allPosts})
    return JsonResponse({'object_list': t})




def edit_post(request, pk):
    get_post = get_object_or_404(Post_sale, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None, instance=get_post )
        if form.is_valid():
            new_obj = form.save(commit=False)
            new_obj.author = request.user
            new_obj = form.save()
            messages.success(request, 'Ваше объявление успешно отредактировано.')
            for f in request.FILES.getlist('all_images'):
                data = f.read() #Если файл целиком умещается в памяти
                photo = PostImage(post=new_obj)
                photo.image_data_link.save(f.name, ContentFile(data))
                photo.save()
            return redirect(new_obj)
            success = True
    template = 'edit_post.html'
    context = {
        'get_post': get_post,
        'form': PostForm(instance=get_post),

    }
    return render (request, template, context)

def load_more_data(request):
    offset=int(request.GET['offset'])
    limit=int(request.GET['limit'])
    allPosts = Post_sale.objects.all().filter(published=True).order_by('-created_at')[offset:offset+limit]
    t=render_to_string('ajax/posts.html', {'object_list':allPosts})
    return JsonResponse({'object_list':t})

def load_more_data_sales(request):
    offset=int(request.GET['offset'])
    limit=int(request.GET['limit'])
    allPosts = Post_sale.objects.all().filter(status='2').filter(published=True).order_by('-created_at')[offset:offset+limit]
    t=render_to_string('ajax/posts.html', {'object_list':allPosts})
    return JsonResponse({'object_list':t})

def load_more_data_rent(request):
    offset=int(request.GET['offset'])
    limit=int(request.GET['limit'])
    allPosts = Post_sale.objects.all().filter(status='3').filter(published=True).order_by('-created_at')[offset:offset+limit]
    t=render_to_string('ajax/posts.html', {'object_list':allPosts})
    return JsonResponse({'object_list':t}) 

def load_more_data_ychastki(request):
    offset=int(request.GET['offset'])
    limit=int(request.GET['limit'])
    allPosts = Post_sale.objects.all().filter(type_object='5').filter(published=True).order_by('-created_at')[offset:offset+limit]
    t=render_to_string('ajax/posts.html', {'object_list':allPosts})
    return JsonResponse({'object_list':t})

def load_more_data_doma(request):
    offset=int(request.GET['offset'])
    limit=int(request.GET['limit'])
    allPosts = Post_sale.objects.filter(type_object='2').filter(published=True).order_by('-created_at')[offset:offset+limit]
    t=render_to_string('ajax/posts.html', {'object_list':allPosts})
    return JsonResponse({'object_list':t})

def load_more_data_village(request):
    offset=int(request.GET['offset'])
    limit=int(request.GET['limit'])
    allPosts = Cottvill.objects.filter(published=True)[offset:offset+limit]
    t=render_to_string('ajax/villages.html', {'object_list':allPosts})
    return JsonResponse({'object_list':t})

class VillageSearch (ListView):
    model = Cottvill
    template_name = 'village/village.html'
    context_object_name = 'village'
    """Поиск поселка"""
    def get_queryset(self):
        q = self.request.GET.get('q')
        a = "".join(q[0].upper()) + q[1:]
        return Cottvill.objects.filter(title__icontains=a)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context

class PostDeleteView(DeleteView): # Создание нового класса
    model = Post_sale
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')

def delete_post(request, pk):
    post = Post_sale.objects.get(pk=pk)
    post.delete()
    messages.success(request, 'Ваше объявление удалено.')

    return redirect('/')



def subscribe(request):
    success = ''
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно подписались на обновления.')
            form = SubscribeForm()
        else:
            messages.error(request, 'Этот адрес уже подписан на обновления.')
    else:
        form = SubscribeForm()
        
    context = { "form": form, "success": success}

    return redirect('/')

def json_main(request):
    qs = Post_sale.objects.values('id','adress','price')
    structure = json.dumps(list(qs), cls=DjangoJSONEncoder)
    return HttpResponse(qs, content_type='application/json')
   