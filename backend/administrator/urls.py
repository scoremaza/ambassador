from django.urls import include, path

from .views import (AmbassadorAPIView, LinkAPIView,
                    OrderAPIView, ProductGenericAPIView)

urlpatterns = [
    path("ambassadors", AmbassadorAPIView.as_view()),
    path("products", ProductGenericAPIView.as_view()),
    path("products/<str:pk>", ProductGenericAPIView.as_view()),
    path("users/<str:pk>/links", LinkAPIView.as_view()),
    path("orders", OrderAPIView.as_view()),
]
