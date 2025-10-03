from django.db import models
from django.utils import timezone
from cars.models import Car

class Lead(models.Model):
    CONTACT = "contact"
    FINANCING = "financing"
    SHIPPING = "shipping"
    CAR = "car"
    KIND_CHOICES = [
        (CONTACT, "Contact"),
        (FINANCING, "Financing"),
        (SHIPPING, "Shipping"),
        (CAR, "Car lead"),
    ]

    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    message = models.TextField(blank=True)
    car = models.ForeignKey(Car, null=True, blank=True, on_delete=models.SET_NULL)
    extra = models.JSONField(default=dict, blank=True)

    source_url = models.URLField(blank=True)
    user_agent = models.TextField(blank=True)
    ip = models.GenericIPAddressField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.kind} | {self.name}"
