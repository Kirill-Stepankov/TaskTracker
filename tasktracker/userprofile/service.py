from tasktracker.settings import SECRET_KEY
import jwt

class UserService:
    @staticmethod
    def get_user_data(request) -> dict:
        print(request.META)
        access_token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        data = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
        return data
    
    def _get_value_from_jwt(self, request, key) -> str:
        data = self.get_user_data(request)
        return data.get(key)

    def get_user_id(self, request) -> str:
        return self._get_value_from_jwt(request, "user_id")