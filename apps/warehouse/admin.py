from django.contrib import admin

from apps.warehouse.models import Warehouse, Stock, StockRelease

admin.site.register(Warehouse)
admin.site.register(Stock)
admin.site.register(StockRelease)
