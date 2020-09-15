from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse


class AuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        return None
