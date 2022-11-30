from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from core.models import User


class UserSerializer(serializers.ModelSerializer):
    
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    
    
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password", "is_ambassador", "full_name"]
        

    def get_first_name(self, obj):
        return obj.first_name.title()

    def get_last_name(self, obj):
        return obj.last_name.title()

    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"

    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        if instance.is_superuser:
            representation["admin"] = True
        return representation


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}
