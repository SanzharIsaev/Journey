from django.urls import path, include


from apps.users.views import RegisterView, follow_user, unfollow_user, user_list, user_detail


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('users/', user_list, name='user_list'),
    path('users/<int:user_id>/', user_detail, name='user_detail'),
    path('register/', RegisterView.as_view(), name="register"),
    path('users/<int:user_id>/follow/', follow_user, name='follow_user'),
    path('users/<int:user_id>/unfollow/', unfollow_user, name='unfollow_user'),
]
