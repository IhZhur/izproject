import django_filters as df
from .models import Car

class CarFilter(df.FilterSet):
    price_min   = df.NumberFilter(field_name="price", lookup_expr="gte")
    price_max   = df.NumberFilter(field_name="price", lookup_expr="lte")
    year_min    = df.NumberFilter(field_name="year", lookup_expr="gte")
    year_max    = df.NumberFilter(field_name="year", lookup_expr="lte")
    mileage_min = df.NumberFilter(field_name="mileage", lookup_expr="gte")
    mileage_max = df.NumberFilter(field_name="mileage", lookup_expr="lte")
    make       = df.CharFilter(field_name="make", lookup_expr="iexact")
    model      = df.CharFilter(field_name="model", lookup_expr="icontains")
    body_type  = df.CharFilter(field_name="body_type", lookup_expr="iexact")

    ordering = df.OrderingFilter(
        fields=(
            ("price", "price"),
            ("year", "year"),
            ("mileage", "mileage"),
            ("created", "created"),
        ),
        field_labels={"created": "date_added"},
    )

    class Meta:
        model = Car
        fields = []
