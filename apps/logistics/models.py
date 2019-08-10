from django.contrib.auth.models import User
from django.db import models

from apps.engineering.models import Project, ProjectEquipment
from configs import random_code, BID_STATUS, QUOTE_STATUS, DESIGN_TYPE, FABRICATION_STATUS


class LogisticsBid(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_status = models.CharField(max_length=68, choices=BID_STATUS, blank=False, default='Open')
    slug = models.SlugField(null=True, db_index=True, blank=True)
    rfq = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = random_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.vendor.first_name} {self.vendor.last_name}'


class LogisticsQuote(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
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
        return f'{self.project.name}'


class LogisticsQuoteItem(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    quote = models.ForeignKey(LogisticsQuote, on_delete=models.CASCADE)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(ProjectEquipment, on_delete=models.CASCADE)
    quote_status = models.CharField(max_length=68, choices=QUOTE_STATUS, blank=False, default='Open')
    quote_price = models.FloatField(default=0)
    slug = models.SlugField(null=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['quote_price']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = random_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.equipment.name}'
