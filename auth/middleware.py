from django.contrib.auth import get_user_model, login


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
                user = UserModel.objects.create(username=username, is_active=True)

            request.user = user
            login(request, user)

        return self.get_response(request)
