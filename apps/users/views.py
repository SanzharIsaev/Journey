from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.shortcuts import render

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from apps.users.models import FollowUser


def user_list(request):
    """Представление списка пользователей"""
    users = User.objects.annotate(
        post_count=Count('post'),  
        country_count=Count('post__country', distinct=True)  
    )
    return render(request, 'users/user_list.html', {'users': users})


def user_detail(request, user_id):
    """Представление страницы пользователя"""
    user = get_object_or_404(User, id=user_id)
    posts = user.post_set.filter(is_active=True)

    posts_by_country = {}
    for post in posts:
        country_name = post.country.name  
        if country_name not in posts_by_country:
            posts_by_country[country_name] = []
        posts_by_country[country_name].append(post)

    is_following = request.user.following_users.filter(followed_user=user).exists()

    context = {
        'user': user,
        'posts_by_country': posts_by_country,
        'is_following': is_following,  # Добавляем результат в контекст
    }

    return render(request, 'users/user_detail.html', context)


def follow_user(request, user_id):
    followed_user = get_object_or_404(User, id=user_id)
    FollowUser.objects.get_or_create(user=request.user, followed_user=followed_user)
    return redirect('user_detail', user_id=user_id)


def unfollow_user(request, user_id):
    followed_user = get_object_or_404(User, id=user_id)
    FollowUser.objects.filter(user=request.user, followed_user=followed_user).delete()
    return redirect('user_detail', user_id=user_id)


class RegisterView(View):
    """Представление регистрации пользователей"""
    
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')
    
    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка при регистрации. Пожалуйста, проверьте введённые данные.')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
            