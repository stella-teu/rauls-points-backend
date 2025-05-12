from django.urls import path
from .views import Home, CreateUser, LoginUser, ProfilesListView, ProfileDetail, PointEventUpdate

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('register/', CreateUser.as_view(), name='register'),
  path('login/', LoginUser.as_view(), name='login'),
  path('profiles/', ProfilesListView.as_view(), name='profiles-list-create'), 
  path('profiles/<int:id>', ProfileDetail.as_view(), name="profile-detail"),
  path('profiles/<int:id>/points',PointEventUpdate.as_view(), name="update-points"),
  # post	      /profiles/:id/point/	give user points (pass user id through body)
  # get        /profiles/?LeaderBoard=trueOrFalse&Cohort=cohortName&TimeFrame=timeFrame
]