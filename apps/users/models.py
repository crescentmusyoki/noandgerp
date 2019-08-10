from django.contrib.auth.models import User
from django.db import models


class AllowedModel(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name


class AllowedPermission(models.Model):
    name = models.CharField(max_length=55, unique=True)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    models = models.ManyToManyField(AllowedModel)

    def __str__(self):
        return self.name
