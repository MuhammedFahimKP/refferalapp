from django.urls import path 

from . import views

urlpatterns = [
    path('register/',views.UserRegisterApiView.as_view(),name="user-register"),
    path('signin/',views.UserSignInAPIView.as_view(),name="user-signin"),
    path('',views.UserViewAPIView.as_view(),name="user-details"),
    path('refferals/',views.UserRefferalAPIView.as_view(),name="user-refferals")
]