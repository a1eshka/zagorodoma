from django import forms
from django.forms import widgets
from django.template import RequestContext
from django.views.generic import ListView, DetailView, CreateView


from .models import Post_sale,PostImage
from .forms import PostForm
from django.shortcuts import redirect, render
from django.core.files.base import ContentFile


class HomePageView(ListView):
    model = Post_sale
    template_name = 'home.html'
    context_object_name = 'all_posts_list'

class HomeDetailView(DetailView):
    model = Post_sale
    template_name = 'post_detail.html'
    context_object_name = 'post'


class HomeCreateView(CreateView):
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
    




