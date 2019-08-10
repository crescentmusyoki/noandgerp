from django.contrib.auth.models import User
from django.db import models
from simple_history.models import HistoricalRecords

from configs import random_code, BID_STATUS, QUOTE_STATUS, DESIGN_TYPE, FABRICATION_STATUS


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    lead = models.ForeignKey(User, on_delete=models.SET(1))
    description = models.TextField()
    owner_name = models.CharField(max_length=255, null=True, blank=True)
    owner_email = models.EmailField(max_length=55, null=True, blank=True)
    bidding = models.BooleanField(default=False, blank=True)
    logistics_bidding = models.BooleanField(default=False, blank=True)
    members = models.ManyToManyField(User, related_name='project_member', blank=True)
    commissioned = models.BooleanField(default=False)
    slug = models.SlugField(null=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = random_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProjectStage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    stage_status = models.BooleanField(default=False)
    stage_percentage = models.CharField(max_length=20)
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
        return self.project.name


class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    document = models.FileField(upload_to='documents')
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


class ProjectDesign(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    document = models.FileField(upload_to='designs')
    design_type = models.CharField(max_length=68, choices=DESIGN_TYPE, blank=False, default='FEED')
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


class ProjectEquipment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    unit_cost = models.FloatField()
    unit_cost_in = models.CharField(max_length=55)
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    measurement_in = models.CharField(max_length=55)
    weight = models.FloatField()
    weight_in = models.CharField(max_length=55)
    estimated_quantity = models.FloatField()
    description = models.TextField()
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


class ProjectBudget(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    unit_cost = models.FloatField()
    unit_cost_in = models.CharField(max_length=55)
    description = models.TextField()
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


class ProjectBid(models.Model):
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


class ProjectQuote(models.Model):
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


class ProjectQuoteItem(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    quote = models.ForeignKey(ProjectQuote, on_delete=models.CASCADE)
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


class ProjectFabrication(models.Model):
    title = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    team = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    fabrication_status = models.CharField(max_length=68, choices=FABRICATION_STATUS, blank=False, default='Ongoing')
    due_date = models.DateField()
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
        return f'{self.title}'
