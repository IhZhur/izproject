from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class Car(models.Model):
    title = models.CharField(max_length=200)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    body_type = models.CharField(max_length=50)

    # price теперь необязательная, т.к. при SOLD цена может отсутствовать
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    stock_no = models.CharField(max_length=50, blank=True)
    mileage = models.PositiveIntegerField(default=0)
    interior = models.CharField(max_length=100, blank=True)
    exterior = models.CharField(max_length=100, blank=True)
    vin = models.CharField(max_length=32, unique=True)
    transmission = models.CharField(max_length=50, blank=True)
    engine = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)

    is_published = models.BooleanField(default=True)
    is_sold = models.BooleanField("Sold", default=False, db_index=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created", "-id"]
        indexes = [
            models.Index(fields=["make", "model"]),
            models.Index(fields=["year"]),
            models.Index(fields=["body_type"]),
            models.Index(fields=["is_published", "is_sold"]),
        ]

    def clean(self):
        # Если не продано, цена обязательна
        if not self.is_sold and self.price in (None,):
            raise ValidationError({"price": "Price is required when the car is not sold."})

    def save(self, *args, **kwargs):
        if not self.slug:
            base = f"{self.year}-{self.make}-{self.model}-{self.vin}"
            self.slug = slugify(base)[:220]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("car_detail", kwargs={"slug": self.slug})

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="cars/")
    alt = models.CharField(max_length=150, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.car.title} #{self.pk}"