from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views import generic
from requests import request
from .models import Post_sale,PostImage, Ip, HouseAdditional
from .forms import PostForm
from django.shortcuts import get_object_or_404, redirect, render
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class SalesListView(generic.ListView):
    """Вывод постов со статусом Продажа"""
    model = Post_sale
    template_name = 'sales.html'
    context_object_name = 'sales'
    def get_queryset(self):
        return Post_sale.objects.filter(status='1')

class DomaListView(generic.ListView):
    """Вывод постов с типом Дом"""
    model = Post_sale
    template_name = 'doma.html'
    context_object_name = 'doma'
    paginate_by = 6
    def get_queryset(self):
        return Post_sale.objects.filter(type_object='1').order_by('-created_at')

class YchastkiListView(generic.ListView):
    """Вывод постов с типом Участок"""
    model = Post_sale
    template_name = 'ychastki.html'
    context_object_name = 'ychastki'
    def get_queryset(self):
        return Post_sale.objects.filter(type_object='3').order_by('-created_at')

class HomePageView(ListView):
    """Вывод всех постов на главной"""
    model = Post_sale
    template_name = 'home.html'
    context_object_name = 'all_posts_list'
    paginate_by = 6
    def get_queryset(self):
        return Post_sale.objects.filter(published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского класса ListView
        context = super().get_context_data(**kwargs)
        # Дополняем контекст нужным нам значением
        context['sale_status_post'] = Post_sale.objects.filter(status=1).count()
        context['rent_status_post'] = Post_sale.objects.filter(status=2).count()
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


class HomeDetailView(DetailView):
    """Детальная страница поста"""
    model = Post_sale
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        self.object = super(HomeDetailView, self).get_object()
        self.object.views += 1
        self.object.save()
        return self.object

def post_single (request, post):
    post = get_object_or_404(Post_sale)

    fav = bool
    if post.favourites.filter(id=request.user.id).exists():
        fav = True
    return render(request, 'post_detail.html', {'fav': fav})


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
