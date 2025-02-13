from django.shortcuts import redirect

class RoleBasedRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.path == '/' and request.user.role == 'worker':
                return redirect('worker-home')
            elif request.path == '/' and request.user.role == 'contractor':
                return redirect('contractor-home')
        response = self.get_response(request)
        return response