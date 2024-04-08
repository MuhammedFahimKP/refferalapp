
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication


import re

def validate_password(password):
    # define our regex pattern for validation
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"

    # We use the re.match function to test the password against the pattern
    match = re.match(pattern, password)

    # return True if the password matches the pattern, False otherwise
    return bool(match)


class JWTPermissionView:
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]