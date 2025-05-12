from django.urls import path
from .views import Home, CreateUser, LoginUser, ProfilesListView, ProfileDetail

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('register/', CreateUser.as_view(), name='register'),
  path('login/', LoginUser.as_view(), name='login'),
  path('profiles/', ProfilesListView.as_view(), name='profiles-list-create'), 
    # get/put/delete	        /profiles/:id/	indivdual user profile
  path('profiles/<int:id>', ProfileDetail.as_view(), name="profile-detail")
  # ?LeaderBoard=trueOrFalse&Cohort=cohortName&TimeFrame=timeFrame
  # get	        /profiles/:id/point/	shows user points
  # post	      /profiles/:id/point/	give user points (pass user id through body)
]