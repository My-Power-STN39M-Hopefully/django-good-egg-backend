from django.contrib import admin
from .models import Officer, Force, Incident

# Register your models here.
admin.site.register(Officer)
admin.site.register(Force)
admin.site.register(Incident)
