# cars/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Car

class CarSitemap(Sitemap):
    # протокол можно зафиксировать
    protocol = "https"  # опционально; по умолчанию берётся из запроса
    changefreq = "daily"
    priority = 0.8

    def items(self):
        qs = Car.objects.all()
        if hasattr(Car, "is_published"):
            qs = qs.filter(is_published=True)
        # устраняем UnorderedObjectListWarning
        return qs.order_by("-updated", "-id") if hasattr(Car, "updated") else qs.order_by("-id")

    def lastmod(self, o):
        return getattr(o, "updated", None) or getattr(o, "updated_at", None)

    def location(self, obj):
        # используем get_absolute_url() если есть, иначе путь по slug
        try:
            return obj.get_absolute_url()
        except Exception:
            return f"/cars/{obj.slug}/"

class StaticPathSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    def items(self):
        # Явные пути исключают ошибки reverse()
        return ["/", "/cars/", "/about/", "/financing/", "/shipping/",
                "/privacy/", "/terms/", "/contact/", "/thanks/"]
    def location(self, item):
        return item
