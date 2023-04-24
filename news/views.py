from django.shortcuts import redirect, render
from django.views.generic import DetailView, CreateView
from django.views import generic
from .models import *
from .forms import NewsForm
from django.shortcuts import render, get_object_or_404 
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

class NewsListView(generic.ListView):
    """Вывод всех новостей"""
    model = News
    template_name = 'news/news.html'
    context_object_name = 'news'

    def get_queryset(self):
        return News.objects.filter(published=True)[:6]
    
    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского класса ListView
        context = super().get_context_data(**kwargs)
        # Дополняем контекст нужным нам значением
        context['total_data'] = News.objects.filter(published=True).count()
        return context


class NewsCreateView(CreateView):
    """Создание новой новости"""
    form_class = NewsForm
    template_name = 'news/add_news.html'
    model = News

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def image_upload_view(self, request):
        if request.method == 'POST':
            form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, self.template_name, {'form': form, 'img_obj': img_obj})
        else:
            form = NewsForm()
        return render(request, self.template_name, {'form': form})
    
class NewsDetailView(DetailView):
    """Детальная страница Новости"""
    model = News
    template_name = 'news/detail_news.html'
    context_object_name = 'news'

    def get(self, request, *args, **kwargs):

        id = self.kwargs['news_slug']
        news = get_object_or_404(News, slug=id)
        context = {
            'news': news,
        }


        return render(request, 'news/detail_news.html', context)
    
def load_more_data_news(request):
    offset=int(request.GET['offset'])
    limit=int(request.GET['limit'])
    allNews = News.objects.filter(published=True)[offset:offset+limit]
    t=render_to_string('ajax/news.html', {'object_list':allNews})
    return JsonResponse({'object_list':t})

def edit_new(request, pk):
    get_post = get_object_or_404(News, pk=pk, author=request.user)
    if request.method == 'POST':
        form = NewsForm(request.POST or None, request.FILES or None, instance=get_post )
        if form.is_valid():
            new_obj = form.save(commit=False)
            new_obj.author = request.user
            new_obj = form.save()
            messages.success(request, 'Ваша новость успешно отредактирована.')
            return redirect(new_obj)
            success = True
    template = 'news/edit_news.html'
    context = {
        'get_post': get_post,
        'form': NewsForm(instance=get_post),

    }
    return render (request, template, context)

def delete_new(request, pk):
    new = News.objects.get(pk=pk)
    new.delete()
    messages.success(request, 'Ваша публикация удалена.')

    return redirect('/news')