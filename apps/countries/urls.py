from django.urls import path

from .views import CountryListView, CountryDetailView


urlpatterns = [
    path('countries/', CountryListView.as_view(), name='country_list'),
    path('countries/<int:pk>/', CountryDetailView.as_view(), name='country_detail'),
]