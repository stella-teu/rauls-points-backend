from django.contrib import admin
from .models import PointEvent, Cohort, Profile

# Register your models here.
admin.site.register(PointEvent)
admin.site.register(Cohort)
admin.site.register(Profile)