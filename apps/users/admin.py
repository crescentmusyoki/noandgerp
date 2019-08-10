from django.contrib import admin

from apps.users.models import AllowedPermission, AllowedModel

admin.site.register(AllowedPermission)
admin.site.register(AllowedModel)
