from datetime import timezone
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .exceptions import NotYourProfile
from core.models import Profile
from .pagination import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import ProfileSerializer, UpdateProfileSerializer

User = get_user_model()


class ProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    renderer_classes = (ProfilesJSONRenderer,)
    pagination_class = ProfilePagination


class ProfileDetailAPIView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username does not exist")

        serializer = self.serializer_class(profile, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.select_related("user")
    renderer_classes = [ProfileJSONRenderer]
    serializer_class = UpdateProfileSerializer

    def patch(self, request, username):
        try:
            self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username does not exist")

        user_name = request.user.username
        if user_name != username:
            raise NotYourProfile

        data = request.data
        serializer = UpdateProfileSerializer(
            instance=request.user.profile, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



class MyCustomUserViewSet(UserViewSet):
    
    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.deleted_at = timezone.now()
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)