from http.client import HTTPResponse
from multiprocessing import context
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from requests import request
from .forms import UserRegistrationForm
from .models import Profile
from .forms import UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.contrib import messages
from posts.models import Post_sale


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    context_object_name = 'all_posts_list'
    
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request, 'home.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'signup.html', {'user_form': user_form})

@login_required
def favourite_list(request):
    new = Post_sale.objects.filter(favourites=request.user)
    return render(request, 'profile/favourites.html', {'new': new})


@login_required
def favourite_add(request, pk):
    post=get_object_or_404(Post_sale, pk=pk)
    if post.favourites.filter(pk=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required

def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Данные профиля успешно изменены.')
        else:
            messages.error(request, 'Ошибка при изменении данных.')
        return redirect ('edit')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
        return render(request,
                      'profile/edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'profile/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context
