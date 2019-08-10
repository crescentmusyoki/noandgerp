from django.contrib.auth.models import User
from django.db import models

from apps.engineering.models import Project
from configs import random_code


class Warehouse(models.Model):
    name = models.CharField(max_length=55, unique=True)
    location = models.CharField(max_length=255)
    slug = models.SlugField(null=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = random_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Stock(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    unit_cost = models.FloatField()
    unit_cost_in = models.CharField(max_length=55)
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    measurement_in = models.CharField(max_length=55)
    weight = models.FloatField()
    weight_in = models.CharField(max_length=55)
    stock = models.FloatField()
    slug = models.SlugField(null=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = random_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class StockRelease(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    released_by = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    slug = models.SlugField(null=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = random_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.project.name} - {self.stock.name}'
