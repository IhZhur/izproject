from django.db import models

# Create your models here.
from django.db import models
from django.core.cache import cache

CACHE_KEY = 'sitesettings:singleton'

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=120, default='My Site')
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    telegram_chat_id = models.CharField(max_length=64, blank=True, default='')
    chatra_id = models.CharField(max_length=64, blank=True, default='')
    pixel_id = models.CharField(max_length=32, blank=True, default='')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site settings'
        verbose_name_plural = 'Site settings'

    def __str__(self):
        return self.site_name or 'Site settings'

    @classmethod
    def load(cls):
        obj = cache.get(CACHE_KEY)
        if obj:
            return obj
        obj = cls.objects.first() or cls.objects.create()
        cache.set(CACHE_KEY, obj, 600)
        return obj

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(CACHE_KEY)
