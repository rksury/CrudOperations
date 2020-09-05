from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core import exceptions

from crud.models import User


class CreatSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    mobile_number = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True, max_length=32)

    class Meta:
        model = User
        fields = '__all__'

    def validate_password(self, value):
        if value:
            errors = dict()
            try:
                from django.contrib.auth.password_validation import validate_password
                validate_password(password=value, user=User)
            except exceptions.ValidationError as err:
                errors['password'] = list(err.messages)
                raise serializers.ValidationError(err)

        return value

    def create_user(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

    def save(self, **kwargs):
        super().save()


class GetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class PutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
