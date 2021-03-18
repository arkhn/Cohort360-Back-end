from django.contrib.auth import get_user_model


UserModel = get_user_model()

class UserIdentityMiddleware:
    header = "Username"

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        username = request.headers.get(self.header, None)

        if username:
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                pass
            else:
                request.user = user

        return self.get_response(request)
