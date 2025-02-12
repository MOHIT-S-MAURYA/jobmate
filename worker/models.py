from django.db import models
from accounts.models import CustomUser

class Worker(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    experience = models.IntegerField(default=0)
    availability = models.BooleanField(default=True)
    location = models.CharField(max_length=255)
    profile_score = models.FloatField(default=0)
    skills = models.ManyToManyField('Skill', through='WorkerSkill')

class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class WorkerSkill(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('worker', 'skill')
