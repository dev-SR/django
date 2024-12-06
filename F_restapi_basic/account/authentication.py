from django.conf import settings
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions


# def enforce_csrf(request):
#     """
#     Enforce CSRF validation.
#     """
#     check = CSRFCheck()
#     check.process_request(request)
#     reason = check.process_view(request, None, (), {})
#     if reason:
#         raise exceptions.PermissionDenied("CSRF Failed: %s" % reason)


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request):
        try:
            header = self.get_header(request)
            # print(header, request.COOKIES.get("access"))

            if header is None:
                raw_token = request.COOKIES.get("access") or None
            else:
                raw_token = self.get_raw_token(header)  ## Authorization: JWT <token>
            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)
            # enforce_csrf(request)
            return self.get_user(validated_token), validated_token
        except Exception:
            return None
