from django.shortcuts import get_object_or_404, redirect, render
from .models import Constcomp
from django.views.generic import DetailView, CreateView
from django.views import generic
from .forms import ConstcompForm

class ConstcompListView(generic.ListView):
    """Вывод всех строительных компаний"""
    model = Constcomp
    template_name = 'constcomp/catalog.html'
    context_object_name = 'catalog'

    def get_queryset(self):
        return Constcomp.objects.filter(published=True)[:6]
    
    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского класса ListView
        context = super().get_context_data(**kwargs)
        # Дополняем контекст нужным нам значением
        context['total_data'] = Constcomp.objects.filter(published=True).count()
        return context

class ConstcompDetailView(DetailView):
    """Детальная страница строительной компании"""
    model = Constcomp
    template_name = 'constcomp/detail_company.html'
    context_object_name = 'catalog'

    def get(self, request, *args, **kwargs):

        id = self.kwargs['constcomp_slug']
        catalog = get_object_or_404(Constcomp, slug=id)
        context = {
            'catalog': catalog,
        }


        return render(request, 'constcomp/detail_company.html', context)

class ConstcompCreateView(CreateView):
    """Создание нового строительной компании"""
    form_class = ConstcompForm
    template_name = 'constcomp/add_company.html'
    model = Constcomp

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def image_upload_view(self, request):
        if request.method == 'POST':
            form = ConstcompForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, self.template_name, {'form': form, 'img_obj': img_obj})
        else:
            form = ConstcompForm()
        return render(request, self.template_name, {'form': form})

