from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name','phone','updated_at')
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()