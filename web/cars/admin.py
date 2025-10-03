from django.contrib import admin
from .models import Car, CarImage

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [CarImageInline]

    @admin.display(description="Price")
    def price_or_sold(self, obj):
        return "SOLD" if obj.is_sold else obj.price

    list_display = ("title", "make", "model", "year", "price_or_sold", "is_published", "is_sold")
    list_filter = ("year", "body_type", "is_published", "is_sold")
    search_fields = ("title", "make", "model", "vin")

    readonly_fields = ("created", "updated")

    fields = (
        "title", "make", "model", "year", "body_type",
        "price", "is_sold",
        "stock_no", "mileage", "interior", "exterior", "vin",
        "transmission", "engine", "description",
        "slug", "is_published", "created", "updated",
    )