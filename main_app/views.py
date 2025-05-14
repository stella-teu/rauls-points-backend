from django.shortcuts import render
from django.db.models import Sum


# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile, Cohort, PointEvent
from .serializer import UserSerializer, CohortSerializer, PointEventSerializer, ProfileSerializer
from django.shortcuts import get_object_or_404

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': "Welcome to the raul's-point-collector api home route!"}
    return Response(content)
  
class CreateUser(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data["username"])
    default_cohort = Cohort.objects.first()
    profile = Profile.objects.create(user=user,cohort=default_cohort,bio="",is_admin=False)
    refresh = RefreshToken.for_user(user)
    return Response ({
      "refresh": str(refresh),
      "access": str(refresh.access_token),
      "profile": ProfileSerializer(profile).data
    })
  
class LoginUser(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    print("User: ", user)
    if not user:
      return Response({"Error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
      profile = Profile.objects.get(user=user)
      profile_data = ProfileSerializer(profile).data
    except Profile.DoesNotExist:
      profile_data = None  # or return a default, or create one if needed

    refresh = RefreshToken.for_user(user)
    return Response({
      "refresh": str(refresh),
      "access": str(refresh.access_token),
      "profile": profile_data
    })
    

class VerifyUser(APIView):
  permission_classes = [permissions.IsAuthenticated]
  
  def post(self, request):
    user = request.user

    # try:
    #     profile = user.profile  # requires related_name='profile'
    # except Profile.DoesNotExist:
    #     return Response({"error": "Profile not found."}, status=404)
    try:
      profile = Profile.objects.get(user=user)
      profile_data = ProfileSerializer(profile).data
    except Profile.DoesNotExist:
      profile_data = None  # or return a default, or create one if needed

    refresh = RefreshToken.for_user(user)
    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "profile": profile_data,
    })
  
  # def post(self,request):
  #   user=User.objects.get(username=request.user)
  #   refresh=RefreshToken.for_user(user)
  #   return Response ({
  #       "refresh": str(refresh),
  #       "access": str(refresh.access_token),
  #       "user": UserSerializer(user).data,
  #     })


class ProfilesListView(generics.ListAPIView):
  serializer_class = ProfileSerializer
  permission_classes = [permissions.AllowAny]
  
  def get_queryset(self):
        queryset = Profile.objects.filter(is_admin=False).select_related('user', 'cohort')

        # Optional filter by cohort name
        cohort_name = self.request.query_params.get("cohort")
        if cohort_name:
            queryset = queryset.filter(cohort__name__iexact=cohort_name)

        # Leaderboard flag
        leaderboard = self.request.query_params.get("leaderboard")
        if leaderboard and leaderboard.lower() == "true":
            queryset = (
                queryset
                .annotate(total_points_agg=Sum('pointevent__value'))
                .order_by('-total_points_agg')
            )[:10]  # top 10
        return queryset

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = ProfileSerializer
  permission_classes = [permissions.IsAuthenticated]
  lookup_field = 'id'
  
  def get_queryset(self):
    user = self.request.user
    return Profile.objects.filter(user=user)  
  
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return Response({
      "profile" : serializer.data
    })
  
  def perform_update(self, serializer):
    profile = self.get_object()
    if profile.user != self.request.user:
      raise PermissionDenied[{"Message" : "You do not have permission to edit this profile"}]
    serializer.save()
  
  def perform_destroy(self, instance):
    profile = self.get_object()
    if profile.user != self.request.user:
      raise PermissionDenied[{"Message" : "You do not have permission to edit this profile"}]
    profile.user.delete()
    instance.delete()

class PointEventUpdate(APIView):
  permission_classes = [permissions.IsAuthenticated]
  def post(self, request, id):
    profile = get_object_or_404(Profile, id=id)
    request_profile = get_object_or_404(Profile, user=request.user)
    if not request_profile.is_admin:
      raise PermissionDenied("Only admins can award points.")
    value = request.data.get('value')
    context = request.data.get('context', '')
    def is_number(string):
      try:
        float(string)
        return True
      except ValueError:
        return False
    if value is None or not is_number(str(value)):
      return Response({"error": "Points value must be provided and must be an integer."}, status=400)
    event = PointEvent.objects.create(
      profile=profile,
      value=int(value),
      context=context
    )
    return Response(PointEventSerializer(event).data, status=201)