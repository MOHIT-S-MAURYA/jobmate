from django.db import models
from accounts.models import CustomUser

class Contractor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    rating_avg = models.FloatField(default=0)

class Job(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed')
    )
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    wage = models.DecimalField(max_digits=10, decimal_places=2)
    required_skills = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')

class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    )
    worker = models.ForeignKey('worker.Worker', on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('worker', 'job')
