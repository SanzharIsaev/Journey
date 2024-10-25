from django.shortcuts import get_object_or_404, redirect

from django.views.generic import ListView, DetailView

from apps.posts.models import Post

from .models import Country, FollowCountry


class CountryListView(ListView):
    """Представление списка стран"""
    
    model = Country
    template_name = 'countries/country_list.html'
    context_object_name = 'countries'


class CountryDetailView(DetailView):
    """Детальное представление страны"""
    
    model = Country
    template_name = 'countries/country_detail.html'
    context_object_name = 'country'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_following'] = FollowCountry.objects.filter(user=self.request.user, country=self.object).exists() if self.request.user.is_authenticated else False
        
        context['posts'] = Post.objects.filter(country=self.object).order_by('-created_at')
        
        return context

    def post(self, request, *args, **kwargs):
        country = self.get_object()
        if request.POST.get('action') == 'follow':
            FollowCountry.objects.get_or_create(user=request.user, country=country)
        elif request.POST.get('action') == 'unfollow':
            FollowCountry.objects.filter(user=request.user, country=country).delete()
        return redirect('country_detail', pk=country.pk)