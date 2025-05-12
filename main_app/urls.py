from django.urls import path
from .views import Home, CreateUser, LoginUser, ProfilesListView

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('register/', CreateUser.as_view(), name='register'),
  path('login/', LoginUser.as_view(), name='login'),
  path('profiles/', ProfilesListView.as_view(), name='profiles-list-create'), # ?LeaderBoard=trueOrFalse&Cohort=cohortName&TimeFrame=timeFrame
  # get	        /profiles/:id/	indivdual user profile
  # put/delete	/profiles/:id/	edit and delete a profile
  # get	        /profiles/:id/point/	shows user points
  # post	      /profiles/:id/point/	give user points (pass user id through body)
]