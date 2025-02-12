from django.contrib import admin
from .models import Worker,Skill,WorkerSkill
# Register your models here.

admin.site.register(Worker)
admin.site.register(Skill)
admin.site.register(WorkerSkill)