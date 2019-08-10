from django.contrib.auth.models import User
from django.db import models

from apps.engineering.models import Project
from configs import random_code


class Civil(models.Model):
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(User, related_name='assigned_by', on_delete=models.CASCADE)
    cleared_by = models.ForeignKey(User, related_name='cleared_by', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    civil_status = models.CharField(choices=(('Active', 'Active'), ('Complete', 'Complete')), max_length=255)
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
        return f'{self.project.name} - {self.description}'


class Commission(models.Model):
    client_id = models.ForeignKey(User, on_delete=models.CASCADE)
    commissioned_by = models.ForeignKey(User, related_name='commission_by', on_delete=models.CASCADE)
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
