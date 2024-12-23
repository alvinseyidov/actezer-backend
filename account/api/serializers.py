from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from account.models import *

User = get_user_model()



class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['id', 'user', 'image', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

    def validate_user(self, value):
        if self.context['request'].user != value:
            raise serializers.ValidationError("You can only manage your own images.")
        return value

class UserDetailSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'token',
            'first_name',
            'last_name',
            'country',
            'city',
        )

    def get_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token.key


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password',]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"




class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"



class InterestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = "__all__"


class UserRatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRating
        fields = ['id', 'rated_user', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at', 'rated_by']

    def validate(self, data):
        rated_by = self.context['request'].user
        rated_user = data.get('rated_user')

        if rated_by == rated_user:
            raise serializers.ValidationError("You cannot rate yourself.")

        # Check if the user has already rated this user
        if UserRating.objects.filter(rated_by=rated_by, rated_user=rated_user).exists():
            raise serializers.ValidationError("You have already rated this user.")

        return data

    def create(self, validated_data):
        validated_data['rated_by'] = self.context['request'].user
        return super().create(validated_data)