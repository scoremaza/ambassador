from django.urls import path

from .views import (
    ProfileDetailAPIView,
    ProfileListAPIView,
    UpdateProfileAPIView,
)

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="all-profiles"),
    path(
        "user/<str:username>/", ProfileDetailAPIView.as_view(), name="profile-details"
    ),
    path(
        "update/<str:username>/", UpdateProfileAPIView.as_view(), name="profile-update"
    ),
   
]
