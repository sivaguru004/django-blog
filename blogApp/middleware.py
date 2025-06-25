from django.shortcuts import redirect
from django.urls import reverse


class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_respond):
        self.get_respond = get_respond

    def __call__(self, request):
        #check user login
        if request.user.is_authenticated:
            paths_to_redirect = [reverse('blog:login'), reverse('blog:register')]

            if request.path in paths_to_redirect:
                return redirect(reverse('blog:index'))
            
        response = self.get_respond(request)
        return response
    
class RedirectUnauthenticatedUserMiddleware:
    def __init__(self, get_respond):
        self.get_respond = get_respond

    def __call__(self, request):
        paths_to_redirect = [reverse('blog:dashboard')]
        if not request.user.is_authenticated and request.path in paths_to_redirect:
            return redirect(reverse('blog:login'))
            
        response = self.get_respond(request)
        return response