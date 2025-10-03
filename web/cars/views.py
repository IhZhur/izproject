from django.views.generic import TemplateView, DetailView
from django_filters.views import FilterView
from leadforms.forms import CarLeadForm
from .models import Car
from .filters import CarFilter

class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["featured_cars"] = (
            Car.objects.filter(is_published=True)
            .prefetch_related("images")
            .order_by("-created")[:6]
        )
        return ctx

class CarListView(FilterView):
    model = Car
    template_name = "cars/car_list.html"
    context_object_name = "cars"
    paginate_by = 12
    filterset_class = CarFilter

    def get_queryset(self):
        qs = (
            Car.objects.filter(is_published=True)
            .prefetch_related("images")
        )
        # начальная сортировка по новизне, OrderingFilter из фильтра переопределит
        return qs.order_by("-created")

class CarDetailView(DetailView):
    model = Car
    template_name = "cars/car_detail.html"
    context_object_name = "car"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = CarLeadForm()
        return ctx

    def get_queryset(self):
        return Car.objects.filter(is_published=True).prefetch_related("images")
