from django.urls import path
from django.views.generic import TemplateView
from .views import HomeView, CarListView, CarDetailView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path("financing/", TemplateView.as_view(template_name="pages/financing.html"), name="financing"),
    path("shipping/", TemplateView.as_view(template_name="pages/shipping.html"), name="shipping"),
    path("contact/", TemplateView.as_view(template_name="pages/contact.html"), name="contact"),
    path("privacy/", TemplateView.as_view(template_name="pages/privacy.html"), name="privacy"),
    path("terms/", TemplateView.as_view(template_name="pages/terms.html"), name="terms"),

    path("cars/", CarListView.as_view(), name="cars_list"),
    path("cars/<slug:slug>/", CarDetailView.as_view(), name="car_detail"),
]
