from django.contrib import admin
from .models import Officer, Force, Incident
from users.models import CustomUser


# Register your models here.
admin.site.register(Officer)
admin.site.register(Force)
admin.site.register(Incident)
admin.site.register(CustomUser)
