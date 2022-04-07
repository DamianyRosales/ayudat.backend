from rest_framework import serializers
from backend.settings import PASSWORD_HASHERS
from users_api.models import Admin, Professional, Patient, Mod, UserBase
from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.core import exceptions
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer
from django.contrib.auth import get_user_model

# Serializers define the API representation.

class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD

class AuthCustomTokenSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            # Check if user sent email
            if validate_email(email_or_username):
                user_request = get_object_or_404(
                    User,
                    email=email_or_username,
                )

                email_or_username = user_request.username

            user = authenticate(username=email_or_username, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "email or username" and "password"')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs

class AdminSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     user = Admin.objects.create_user(
    #         email=validated_data['email'],
    #         password=validated_data['password'],
    #     )
    #     return user

    class Meta:
        model = Admin
        fields = '__all__'
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance,validated_data)


    


class ModSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Mod
        fields = '__all__'

    # def create(self, validated_data):
    #     user = UserBase.objects.create_user(
    #         email=validated_data['email'],
    #         password=validated_data['password'],
    #     )
    #     return user
    



    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance,validated_data)
    


class ProfessionalSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     user = UserBase.objects.create_user(
    #         email=validated_data['email'],
    #         password=validated_data['password'],
    #     )
    #     return user

    class Meta:
        model = Professional
        fields = '__all__'
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance,validated_data)
    

class Professional2Serializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     user = UserBase.objects.create_user(
    #         email=validated_data['email'],
    #         password=validated_data['password'],
    #     )
    #     return user

    class Meta:
        model = Professional
        fields = ['document1','document2']
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance,validated_data)
    


class PatientSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     user = UserBase.objects.create_user(
    #         email=validated_data['email'],
    #         password=validated_data['password'],
    #     )
    #     return user

    class Meta:
        model = Patient
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance,validated_data)
    

