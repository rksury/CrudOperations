from rest_framework import status
from rest_framework.response import Response

from .serializers import PutSerializer, GetSerializer, CreatSerializer
from crud.models import User


def create_user(data):
    ser = CreatSerializer(data=data)
    if ser.is_valid():
        ser.save()
        user = ser.instance
        user.set_password(ser.validated_data['password'])
        user.save()
        user_ser = GetSerializer(user)
        return Response(user_ser.data, status=status.HTTP_201_CREATED)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


def get_user(user_id):
    if user_id:
        try:
            target_user = User.objects.get(id=user_id)
            serializer = GetSerializer(target_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'user_not_exists'}, status=status.HTTP_404_NOT_FOUND)
    else:
        target_user = User.objects.all()
        serializer = GetSerializer(target_user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

def update_user(user, user_id, data):
    if user.is_superuser is False:
        user_id = user.id
    try:
        user_update = User.objects.get(id=user_id)
        serializer = PutSerializer(user_update, data=data, context={'user': user})
        if serializer.is_valid():
            user_updated = serializer.save()
            get_serializer = GetSerializer(user_updated,)
            return Response(get_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({'error': 'user_not_exists'}, status=status.HTTP_404_NOT_FOUND)


def delete_user(user_id):
    try:
        target_user = User.objects.get(id=user_id)
        target_user.delete()
        return Response({'Message': 'user deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'error': 'user_not_exists'}, status=status.HTTP_404_NOT_FOUND)
