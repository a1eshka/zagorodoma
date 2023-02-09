import datetime
from msilib.schema import PublishComponent
from multiprocessing import context
import os
import parser
from pickle import FALSE
from re import template
from sre_constants import SUCCESS
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView
from django.views import generic
from requests import request
from .models import Post_sale,PostImage, Type_object, Status, Land_status, House_material, District, Cottvill
from .forms import PostForm, VillageForm
from django.shortcuts import get_object_or_404, redirect, render
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from datetime import date
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib import messages


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

class SalesListView(generic.ListView):
    """Вывод постов со статусом Продажа"""
    model = Post_sale
    template_name = 'sales.html'
    context_object_name = 'sales'
    def get_queryset(self):
        return Post_sale.objects.filter(status='2').filter(published=True).order_by('-created_at')

class DomaListView(generic.ListView):
    """Вывод постов с типом Дом"""
    model = Post_sale
    template_name = 'doma.html'
    context_object_name = 'doma'
    paginate_by = 6
    def get_queryset(self):
        return Post_sale.objects.filter(type_object='2').filter(published=True).order_by('-created_at')

class YchastkiListView(generic.ListView):
    """Вывод постов с типом Участок"""
    model = Post_sale
    template_name = 'ychastki.html'
    context_object_name = 'ychastki'
    def get_queryset(self):
        return Post_sale.objects.filter(type_object='3').filter(published=True).order_by('-created_at')

class HomePageView(FilterMain, ListView):
    """Вывод всех постов на главной"""
    model = Post_sale
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
        context['total_data'] = Post_sale.objects.filter(published=True).count()
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
    model = Post_sale
    template_name = 'post_detail.html'
    context_object_name = 'post'

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
    allPosts=Post_sale.objects.all().filter(published=True).order_by('-created_at')
    if minLand_area:
        allPosts=allPosts.filter(land_area__gte=minLand_area)
    if maxLand_area:
        allPosts=allPosts.filter(land_area__lte=maxLand_area)
    if minPrice:
        allPosts=allPosts.filter(price__gte=minPrice)
    if maxPrice:
        allPosts=allPosts.filter(price__lte=maxPrice)
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
    get_post = Post_sale.objects.get(pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None, instance=get_post )
        if form.is_valid():
            new_obj = form.save(commit=False)
            new_obj.author = request.user
            new_obj = form.save()
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




        

