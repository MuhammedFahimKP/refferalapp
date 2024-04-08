from django.db import models
from django.contrib.auth.models import  AbstractBaseUser,PermissionsMixin

from rest_framework_simplejwt.tokens import RefreshToken

import uuid

from .managers import UserManager






class User(AbstractBaseUser,PermissionsMixin):

    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email          = models.EmailField(unique=True,db_index=True)
    name           = models.CharField(max_length=150)
 
    """
    required fields 

    """
    registered_at  = models.DateTimeField(auto_now_add=True)
    last_login     = models.DateTimeField(auto_now=True)

    "sub admin field"
    
    is_staff       = models.BooleanField(default=False)
    
    "super admin field"
    
    is_superuser   = models.BooleanField(default=False)

    "active field "
    
    is_active      = models.BooleanField(default=False)

    objects        = UserManager() 

    """
       we are teling that model required fields and 
       usernamefield      
    """ 

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['name']
    
        

    def __str__(self) -> str:
        return f"{self.name}"
 
    """
        tokens property function to get access and refresh jwt tokens of user "
    """  
    @property
    def tokens(self) -> dict[str : str]:
        
        """Allow us to get a user's json web token by calling user.token."""

        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}

