"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from leadforms.views import ContactView, FinancingView, ShippingView, CarLeadView
from rest_framework.routers import DefaultRouter
from cars.api import CarViewSet
from django.contrib.sitemaps.views import sitemap
from cars.sitemaps import CarSitemap, StaticPathSitemap
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularYAMLAPIView,
    SpectacularJSONAPIView,
)

def healthz(_): return HttpResponse("ok")
router = DefaultRouter()
router.register("cars", CarViewSet, basename="car")

def sentry_debug(_): 1/0

sitemaps = {"cars": CarSitemap(), "static": StaticPathSitemap()}

urlpatterns = [
    path("sentry-debug/", sentry_debug),
    path("healthz/", healthz, name="healthz"),
    path("admin/", admin.site.urls),
    path("contact/", ContactView.as_view(), name="contact"),
    path("financing/", FinancingView.as_view(), name="financing"),
    path("shipping/", ShippingView.as_view(), name="shipping"),
    path("cars/<slug:slug>/lead/", CarLeadView.as_view(), name="car_lead"),
    path("thanks/", TemplateView.as_view(template_name="pages/thanks.html"), name="thanks"),
    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("", include("cars.urls")),
    path("api/", include(router.urls)),
    # схема
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema.yaml", SpectacularYAMLAPIView.as_view(), name="schema-yaml"),
    path("api/schema.json", SpectacularJSONAPIView.as_view(), name="schema-json"),

    # UI
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
