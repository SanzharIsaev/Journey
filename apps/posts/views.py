from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django import views

from taggit.models import Tag

from django.db.models import Q

from apps.comments.forms import CommentForm
from apps.countries.models import FollowCountry
from apps.users.models import FollowUser

from .forms import PostForm, PostImageForm

from .models import Likes, Post, PostImage, FollowTag



class HomeView(generic.TemplateView):
    """Представление главной страницы"""
    
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            followed_tags = FollowTag.objects.filter(user=self.request.user).values_list('tag', flat=True)
            followed_users = FollowUser.objects.filter(user=self.request.user).values_list('followed_user', flat=True)
            followed_countries = FollowCountry.objects.filter(user=self.request.user).values_list('country', flat=True)

            context['posts'] = Post.objects.filter(
                Q(tags__id__in=followed_tags) | 
                Q(user__id__in=followed_users) | 
                Q(country__id__in=followed_countries),
                is_active=True  
            ).distinct().order_by('-created_at')
        else:
            context['posts'] = Post.objects.filter(is_active=True).order_by('-created_at') 

        return context


class PostListView(views.View):
    
    def get(self, request):
        posts = Post.objects.filter(is_active=True).order_by('-created_at')
        return render(request, "posts/post_list.html", {"posts": posts})


class PostDetailView(generic.DetailView):
    """Детальное представление поста"""
    
    model = Post
    template_name = 'posts/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        context['images'] = self.object.images.all()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
        else:
            return self.get(request, *args, **kwargs)


class PostCreateView(generic.CreateView):
    """Представление создания поста"""
    
    model = Post
    form_class = PostForm
    template_name = 'posts/post_create.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_image_form'] = PostImageForm() 
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        post = form.save()  

        for tag in form.cleaned_data['tags']:
            post.tags.add(tag)

        images = self.request.FILES.getlist('image') 
        for image in images:
            PostImage.objects.create(post=post, image=image) 

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return HttpResponseForbidden("Администраторы не могут создавать посты")
        return super().dispatch(request, *args, **kwargs)


class PostUpdateView(generic.UpdateView):
    """Представление обновления поста"""
    
    model = Post
    form_class = PostForm
    template_name = 'posts/post_update.html'
    success_url = reverse_lazy('home')
    
    def get_initial(self):
        initial = super().get_initial()
        initial['tags'] = ', '.join(str(tag) for tag in self.object.tags.all())
        return initial

    def author(self, request, *args, **kwargs):
        # Проверка пользователя на авторство поста
        post = self.get_object()
        if post.user != request.user:
            return HttpResponseForbidden("Вы не можете редактировать этот пост")
        return super().dispatch(request, *args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_images'] = self.object.images.all()  # Получаем существующие изображения
        context['post_image_form'] = PostImageForm()  # Форма для добавления новых изображений
        return context

    def form_valid(self, form):
        # Сначала сохраняем пост
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()


        images = self.request.FILES.getlist('image') 
        for image in images:
            PostImage.objects.create(post=post, image=image) 

        return super().form_valid(form)


class PostDeleteView(generic.DeleteView):
    """Представление удаления поста"""
    
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('home')

    def author(self, request, *args, **kwargs):
        # Проверка пользователя на авторство поста
        post = self.get_object()
        if post.user != request.user:
            return HttpResponseForbidden("Вы не можете удалить этот пост.")
        return super().dispatch(request, *args, **kwargs)



def tagged(request, pk):
    tag = get_object_or_404(Tag, id=pk)
    posts = Post.objects.filter(tags=tag).order_by('-created_at')
    
    is_following = False
    if request.user.is_authenticated:
        is_following = FollowTag.objects.filter(user=request.user, tag=tag).exists()
    
    context = {
        'tag': tag,
        'posts': posts,
        'is_following': is_following
    }
    
    return render(request, 'posts/tag_detail.html', context)

def follow_tag(request, pk):
    tag = get_object_or_404(Tag, id=pk)
    FollowTag.objects.get_or_create(user=request.user, tag=tag)
    return redirect('tagged', pk=pk)

def unfollow_tag(request, pk):
    tag = get_object_or_404(Tag, id=pk)
    FollowTag.objects.filter(user=request.user, tag=tag).delete()
    return redirect('tagged', pk=pk)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class AddLike(views.View):
    
    def get(self, request, pk):
        ip_client = get_client_ip(request)
        
        pos = get_object_or_404(Post, pk=pk)

        if Likes.objects.filter(ip=ip_client, pos=pos).exists():
            return redirect(reverse('post_detail', args=[pk]))

        new_like = Likes()
        new_like.ip = ip_client
        new_like.pos = pos
        new_like.save()
        
        return redirect(reverse('post_detail', args=[pk]))


class DeleteLike(views.View):
    
    def get(self, request, pk):
        ip_client = get_client_ip(request)
        
        # Получаем пост по первичному ключу
        pos = get_object_or_404(Post, pk=pk)

        try:
            # Ищем лайк по IP и посту
            like = Likes.objects.get(ip=ip_client, pos=pos)
            like.delete()
        except Likes.DoesNotExist:
            pass
        
        return redirect(reverse('post_detail', args=[pk]))