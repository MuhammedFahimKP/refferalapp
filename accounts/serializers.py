
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password



from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated,NotFound,AuthenticationFailed


from refferals.models import ReferralCode,ReferralRelationship
from .exceptions import AlreadyExist 
from .utils import validate_password




USER_MODEL = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    
    email   = serializers.EmailField()
    name     = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8 , max_length=10)
    ref_code = serializers.CharField(write_only=True)
    id       = serializers.CharField(read_only=True)
    
    def validate(self, data):
        
        user = USER_MODEL.objects.filter(email=data['email'])
        
        
        
        if user.exists():    
            raise AlreadyExist({ 'email' : 'user with this already exist'})   
        
        if not validate_password(data['password']):
    
            raise serializers.ValidationError({'password':'not matching alphanumerics '})
        
        
        refcode = ReferralCode.objects.filter(token=data['ref_code'])
        
        if not refcode.exists():
            
            raise NotAuthenticated({'ref_code' : 'please provide valid ref code'})
             
        
            
        return data
    
    
    def create(self, validated_data):
        
        insance = USER_MODEL.objects.create(
           
            name=validated_data['name'], 
            email=validated_data['email'], 
            password=make_password(validated_data['password']), 
            
        )
        
        ref_code = ReferralCode.objects.filter(token=validated_data['ref_code'])
        # create relationship for inviter and invited persone
        
        ReferralRelationship(
               referrer =ref_code[0].user, referrered = insance , refer_token=ref_code[0]
        ).save()
        
        
        
            
        return insance
    
    
    class Meta:
        
        model = USER_MODEL
        fields = [
            'id',
            'name',
            'email',
            'password',
            'ref_code',
        
        ]


class UserSignInSerializer(serializers.Serializer):

    # access   = serializers.CharField(read_only=True)
    # refresh  = serializers.CharField(read_only=True)
    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True,min_length=8 , max_length=10)
    
    def validate(self, data):
        
        user = USER_MODEL.objects.filter(email=data['email'])
        
        if not user.exists():
            
            raise  NotFound({ 'email':'user with this mail id not found'})
        
        user = user.first()
        
        if  user.check_password(data['password']) == False :
            raise AuthenticationFailed({'password':'incorrect password'})
        
        if  user.is_active == False:
            raise AuthenticationFailed({'email':'please active your account'})
        
        return user
        
        
    
    
    
    

    
            


class UserViewSerailizer(serializers.ModelSerializer):
    
    ref_code        = serializers.SerializerMethodField()
    registered_at   = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    
    def get_ref_code(self,obj):
        return obj.referralcode_set.all()[0].token
    
    
    class Meta:
        
        model = USER_MODEL
        
        fields = [
            'email',
            'name',
            'ref_code',
            'registered_at'
            
        ]
        

class UserReferalsViewSerailizer(serializers.ModelSerializer):
    
    ref_code        = serializers.SerializerMethodField()
    registered_at   = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    
    def get_ref_code(self,obj):
        return obj.referralcode_set.all()[0].token
    
    
    class Meta:
        
        model = USER_MODEL
        
        fields = [
            'email',
            'name',
            'ref_code',
            'registered_at'
            
        ]

# class UserRefferalsSerailizers(serializers.ModelSerializer):
    
     
     
     
#     class Meta:
         
#          fields = [
             
#          ]       
              
        
    
    
    