from django.contrib import admin

from apps.logistics.models import LogisticsBid, LogisticsQuote, LogisticsQuoteItem

admin.site.register(LogisticsBid)
admin.site.register(LogisticsQuote)
admin.site.register(LogisticsQuoteItem)
