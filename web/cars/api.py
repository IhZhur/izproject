# cars/api.py
from django.db.models import Prefetch, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from rest_framework import serializers, viewsets, permissions
from django_filters import rest_framework as filters

from .models import Car, CarImage


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ("id", "image", "alt", "order")


class CarSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)  # nested to-many

    class Meta:
        model = Car
        fields = "__all__"


class CarFilter(filters.FilterSet):
    year_min = filters.NumberFilter(field_name="year", lookup_expr="gte")
    year_max = filters.NumberFilter(field_name="year", lookup_expr="lte")
    price_max = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Car
        fields = ["make", "model", "body_type", "transmission"]


@method_decorator(cache_control(public=True, max_age=60), name="list")
@method_decorator(cache_control(public=True, max_age=60), name="retrieve")
class CarViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = CarSerializer
    filterset_class = CarFilter
    ordering_fields = ["price", "year", "created", "updated", "mileage"]
    search_fields = ["title", "make", "model", "vin", "stock_no", "description"]

    lookup_field = "slug"
    lookup_value_regex = r"[-a-zA-Z0-9_]+"

    def get_queryset(self):
        images_qs = CarImage.objects.order_by("order", "id")
        qs = Car.objects.all().prefetch_related(Prefetch("images", queryset=images_qs))
        if hasattr(Car, "is_published"):
            qs = qs.filter(is_published=True)
        return qs

    def get_object(self):
        from rest_framework.exceptions import NotFound

        lookup = self.kwargs.get(self.lookup_field)
        qs = self.get_queryset()
        # сперва пробуем как id, потом как slug
        try:
            return qs.get(pk=int(lookup))
        except (ValueError, Car.DoesNotExist):
            obj = qs.filter(slug=lookup).first()
            if not obj:
                raise NotFound("Car not found")
            return obj
