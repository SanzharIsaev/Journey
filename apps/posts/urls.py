from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post_create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('tags/<int:pk>/', views.tagged, name='tagged'),
    path('tags/<int:pk>/follow/', views.follow_tag, name='follow_tag'),
    path('tags/<int:pk>/unfollow/', views.unfollow_tag, name='unfollow_tag'),
    path('post/<int:pk>/add_like/', views.AddLike.as_view(), name='add_like'),
    path('post/<int:pk>/delete_like/', views.DeleteLike.as_view(), name='delete_like'),
]