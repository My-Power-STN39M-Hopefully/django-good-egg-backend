from django.db import models

# Create your models here.
class Incident(models.Model):
  YES = 'y'
  NO = 'n'
  yes_or_no = (
    (YES, 'yes'),
    (NO, 'no'),
  )
  category = models.CharField(max_length=100)
  officers =  models.ForeignKey(Officer, on_delete=models.CASCADE, related_name='officer')
  date = models.CharField(max_length=100)
  time = models.CharField(max_length=100)
  location = models.CharField(max_length=100)
  formal_complaint = models.CharField(max_length=100)
  formal_complaint_number = models.CharField(max_length=100, choices=yes_or_no, default=NO)
  witnesses_present = models.CharField(max_length=100, choices=yes_or_no, default=NO)
  witnesses_information = models.CharField(max_length=100)
  User_id = models.CharField(max_length=100)
  private = models.CharField(max_length=100, choices=yes_or_no, default=NO)
  bad_apple = models.CharField(max_length=100, default = True)

  def __str__(self):
    return f'{self.category} - {self.officer} - {self.date} {self.time}'
  
  
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