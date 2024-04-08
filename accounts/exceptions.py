from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException
from rest_framework import status

class AlreadyExist(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Already Exist')
    default_code = 'already_exist'
    
    

        