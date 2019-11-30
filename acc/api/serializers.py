from django.contrib.auth import authenticate, get_user_model

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'bio', 'website')


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class UserDetailSerializer(ModelSerializer):
    id = serializers.ReadOnlyField()
    follower_count = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'bio',
                  'website',
                  'follower_count')

    def get_follower_count(self, obj):
        return 0

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.website = validated_data.get('website', instance.website)

        instance.save()
        return instance
