from django.contrib import admin

# Register your models here.
from apps.construction.models import Civil, Commission

admin.site.register(Civil)
admin.site.register(Commission)
