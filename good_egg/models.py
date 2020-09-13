from django.db import models
from users.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.core.exceptions import ValidationError

def date_must_be_past(date):
    if date > timezone.now().date():
        raise ValidationError("Date cannot be in the future.")

class Force(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    precinct_phone_number = PhoneNumberField(
        null=True, blank=False, unique=False)
    precinct_address = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Officer(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(null=True, validators=[date_must_be_past])
    badge_number = models.CharField(max_length=100, null=True)
    nationality = models.CharField(max_length=100, null=True)
    race = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100, null=True)
    force = models.ForeignKey(Force, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id} {self.first_name} {self.last_name}, {self.badge_number} {self.force}.  {self.active}'


class Incident(models.Model):
    category = models.CharField(max_length=100)
    officers = models.ManyToManyField(Officer, blank=True)
    officer_description = models.TextField()
    date = models.DateField(validators=[date_must_be_past])
    time = models.TimeField()
    location = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    formal_complaint = models.BooleanField(default=False)
    formal_complaint_number = models.CharField(max_length=100, null=True, blank=True)
    witnesses_present = models.BooleanField(default=False)
    witnesses_information = models.TextField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    private = models.BooleanField(default=False)
    bad_apple = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.category} - {self.date} {self.time}'
