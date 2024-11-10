from django.contrib import admin

from .models import Post



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'is_active']
    list_filter = ['user', 'created_at']
    list_editable = ['is_active']

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if request.user.is_superuser:
            return ['is_active']  
        return fields  

    def has_change_permission(self, request, obj=None):
        return True 

    def has_delete_permission(self, request, obj=None):
        return not request.user.is_superuser
