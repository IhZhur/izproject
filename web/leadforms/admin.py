# web/leadforms/admin.py
from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("created_at","kind","name","email","phone","ip")
    list_filter = ("kind",)
    search_fields = ("name","email","phone","message")
