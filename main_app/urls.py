from django.urls import path
from .views import (Home, 
                    ListProfile, 
                    ProfileDetail,
                    PointEventEdit,
                    )

urlpatterns = [
  path('', Home.as_view(), name='home'),
]