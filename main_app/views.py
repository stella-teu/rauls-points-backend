from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile, Cohort, PointEvent
from .serializer import UserSerializer, CohortSerializer, PointEventSerializer, PointEventWriteSerializer, ProfileSerializer, ProfileWriteSerializer


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
    Profile.objects.create(user=user,cohort=default_cohort,bio="",is_admin=False)
    refresh = RefreshToken.for_user(user)
    return Response ({
      "refresh": str(refresh),
      "access": str(refresh.access_token),
      "user": response.data,
    })
  
class LoginUser(APIView):
  permission_classes = [permissions.AllowAny]
  def post(self,request):
    username = request.data.get("username")
    password = request.data.get("password")
    user=authenticate(username=username,password=password)
    if user:
      refresh=RefreshToken.for_user(user)
      return Response ({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": UserSerializer(user).data,
      })
    return Response ({"Error":"Invalid Credentials"},status=status.HTTP_401_UNAUTHORIZED)
  
class VerifyUser(APIView):
  permission_classes = [permissions.IsAuthenticated]
  def post(self,request):
    user=User.objects.get(username=request.user)
    refresh=RefreshToken.for_user(user)
    return Response ({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": UserSerializer(user).data,
      })
    
  
