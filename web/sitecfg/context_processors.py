from .models import SiteSettings
def site_settings(request):
    return {'SITE': SiteSettings.load()}