"""
Security Middleware + Cookie Banner (Solution)
Compatible with Django 5
"""

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import path


class AppTokenMiddleware:
    """
    Custom class-based middleware.
    Blocks POST requests if 'X-APP-TOKEN' header is missing.
    Allows:
        - All GET requests
        - POST requests only if header exists
    """

    def __init__(self, get_response):
        # Store get_response to continue middleware chain
        self.get_response = get_response

    def __call__(self, request):
        # Block only POST requests when header missing
        if request.method == "POST":
            token = request.headers.get("X-APP-TOKEN")
            if not token:
                return HttpResponse("Forbidden", status=403)

        # Continue request pipeline
        response = self.get_response(request)
        return response


def accept_consent(request):
    """
    GET /consent/accept/?next=/some/path/
    Sets cookie 'cookie_consent=yes'
    Redirects to 'next' or '/' if missing.
    """

    # Safe default to '/'
    nxt = request.GET.get("next") or "/"

    # Create redirect response properly
    response = redirect(nxt)

    # Correct cookie key and value
    response.set_cookie("cookie_consent", "yes")

    return response


urlpatterns = [
    path("consent/accept/", accept_consent, name="accept_consent"),
]