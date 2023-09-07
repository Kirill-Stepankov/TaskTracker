from tasktracker.settings import SECRET_KEY
import jwt
from jwt import exceptions
from rest_framework.exceptions import AuthenticationFailed

class UserService:
    @staticmethod
    def get_user_data(request) -> dict:
        access_token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        try:    
            data = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
        except exceptions.DecodeError as e:
            raise AuthenticationFailed(code=401, detail=str(e))
        return data
    
    def _get_value_from_jwt(self, request, key) -> str:
        data = self.get_user_data(request)
        return data.get(key)

    def get_user_id(self, request) -> str:
        return self._get_value_from_jwt(request, "user_id")