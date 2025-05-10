from django.db import models
# from pillow import ImageField

# Create your models here.

class Cohort (models.Model):
    name = models.CharField(max_length=50)
    # created_at = models.TimeField()
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    # user_id = models.ForeignKey()
    bio = models.CharField(max_length=250)
    # profile_pic = models.ImageField()
    is_admin = models.BooleanField()
    cohort_id = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    created_at = models.TimeField()
    updated_at = models.TimeField()
    
    def __str__(self):
        return self.name

class PointEvent(models.Model):
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.IntegerField()
    context = models.CharField(max_length = 100)
    created_at = models.TimeField()
    
    def __str__(self):
        return self.value
