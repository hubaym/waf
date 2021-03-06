from django.contrib.auth import get_user_model
from classes.neo_classes.usertoneo import UserToNeo

class CustomUserAuth(object):

    def authenticate(self, username=None, password=None):
        try:
            user = get_user_model().objects.get(email=username)
            
            print("I found this user",user.id)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            print("there is no any user like this")
            return None

    def get_user(self, user_id):
        try:
            user = get_user_model().objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except get_user_model().DoesNotExist:
            return None
    