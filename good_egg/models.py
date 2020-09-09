from django.db import models

# Create your models here.


class Incident(models.Model):
    category = models.CharField(max_length=100)
    officers = models.ManyToManyField()
    officer_description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100, null=True)
    description = models.TextField()
    formal_complaint = models.CharField(max_length=100, null=True,)
    formal_complaint_number = models.CharField(max_length=100, null=True)
    witnesses_present = models.BooleanField(default=False)
    witnesses_information = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    private = models.BooleanField(default=False)
    bad_apple = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.category} - {self.date} {self.time}'


class Officer(models.Model):
    fist_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.CharField(max_length=100)
    badge_number = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100, default='N/A')
    race = models.CharField(max_length=100, default='N/A')
    gender = models.CharField(max_length=100)
    force = models.CharField(max_length=100)
    active = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}, {self.badge_number} {self.force}.  {self.active}'
