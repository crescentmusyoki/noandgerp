from django.contrib.auth.models import User
from django.db import models

from apps.engineering.models import Project, ProjectFabrication
from configs import random_code, SURVEY_TYPE, QUESTION_TYPE


class Survey(models.Model):
    name = models.CharField(max_length=55, unique=True)
    survey_type = models.CharField(max_length=68, choices=SURVEY_TYPE, blank=False, default='Shipping')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
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


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.TextField()
    question_type = models.CharField(max_length=68, choices=QUESTION_TYPE, blank=False, default='1')
    status = models.BooleanField(default=False)
    slug = models.SlugField(null=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['question']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = random_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question


class SurveyQuestionAnswer(models.Model):
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    task_given = models.ForeignKey(ProjectFabrication, on_delete=models.CASCADE)
    answer = models.TextField()
    slug = models.SlugField(null=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['question']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = random_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question.question


class HelpIssue(models.Model):
    name = models.CharField(max_length=255)
    problem = models.TextField()
    priority = models.CharField(max_length=55)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_assigned_by', blank=True,
                                    null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_created_by', blank=True,
                                   null=True)
    status = models.CharField(max_length=255, default='Unresolved')
    solution = models.TextField(blank=True, null=True)
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
        return self.name
