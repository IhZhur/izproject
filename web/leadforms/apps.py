# web/leadforms/apps.py
from django.apps import AppConfig
class LeadsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "leadforms"
    label = "leads"
    verbose_name = "Leads"
