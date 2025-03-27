# contractor/admin.py file is used to register the models in the admin panel.
from django.contrib import admin
from .models import Contractor,Job,Application
# Register your models here.
admin.site.register(Contractor)
admin.site.register(Job)
admin.site.register(Application)
