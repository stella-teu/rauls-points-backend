from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Cohort (models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    bio = models.CharField(max_length=250)
    # profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    is_admin = models.BooleanField()
    
    def __str__(self):
        
        return self.user.username

class PointEvent(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.IntegerField()
    context = models.CharField(max_length = 100)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.profile.user.username
