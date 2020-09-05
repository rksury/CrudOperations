from rest_framework.decorators import APIView

from .services import create_user, get_user, update_user, delete_user


class UserView(APIView):

    def post(self, request):
        return create_user(data=request.data)

    def get(self, request, user_id=None):
        if not user_id:
            user_id = request.user.pk
        return get_user(user_id)

    def put(self, request, user_id):
        return update_user(request.user, user_id, request.data)

    def delete(self, request, user_id=None):
        if not user_id:
            user_id = request.user.pk
        return delete_user(user_id)
