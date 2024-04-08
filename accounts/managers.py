
import secrets
from django.contrib.auth.models import BaseUserManager

from refferals.models import ReferralRelationship, ReferralCode


class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        # checking if user add all fields
        
      
        if not email:
            raise ValueError("Users must have an email address!")
        
        # getting referral code and if code is not exist return error
        
        
       
        
       
 
            # create user
        user = self.model(
            name=name, 
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        
    
    
        self.create_reftoken(user)
        

        return user
    

    def create_superuser(self, name, email, password=None):
        # admin can use defunct referral code
        user = self.model(email=email,name=name,password=password )
        # set password and andmin things
        
        
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        # create refferal code for admin
        self.create_reftoken(user)
        
        return user

    # method for creating tokens
    def create_reftoken(self, user):
        token = secrets.token_urlsafe(20)
        ReferralCode(token=token, user=user).save()