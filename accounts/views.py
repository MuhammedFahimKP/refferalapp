from rest_framework import generics,status
from rest_framework.response import Response

from .serializers import UserRegisterSerializer,UserSignInSerializer,UserViewSerailizer
from .utils import JWTPermissionView


class UserRegisterApiView(generics.GenericAPIView):
    #my user serializer class for creating users
    serializer_class = UserRegisterSerializer

    #post method only allow

    def post(self,request):

        #taking the post data   
        user_data = self.request.data

        #sending the data to the serializer
        serializer = self.serializer_class(data=user_data)
        

        """
        checking serializer is valid if serialzer is not valid it will send serailizor error with http 400   

        """    
        if serializer.is_valid(raise_exception=True):

            #creating new user  object using serializer create method
            
            serializer.save()

            #taking the serializer data for response sending activation link

            user = serializer.data
            
            #calling thread class to send email

        
            
            #returning the response with http 201
          
            return Response({'user_id':user['id']},status=status.HTTP_201_CREATED) 
           
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

    
class UserSignInAPIView(generics.GenericAPIView):

        serializer_class = UserSignInSerializer

        #allow only post method
        def post(self,request):
            #passing the data to the serializer
            serialzer = self.serializer_class(data=self.request.data)
            
            #if serializer valid then it will send a data with http 200 
            if serialzer.is_valid(raise_exception=True):
                
                user = serialzer.validated_data 
                
                
                data = {
                    'email':user.email,
                    'name':f"{user.name}",
                    'access':str(user.tokens.get('access')),
                    'refresh':str(user.tokens.get('refresh'))
                }
            
                
                return Response(data,status=status.HTTP_200_OK)
            
            #otherwise it will send data serializer error with http 400 
            return Response(serialzer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserViewAPIView(JWTPermissionView,generics.GenericAPIView):
    
    def get(self, request):
        user = request.user
        serializer = UserViewSerailizer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRefferalAPIView(JWTPermissionView,generics.GenericAPIView):
    
    
    def get(self, request):
        users = request.user.invited
        serializer = UserViewSerailizer(users,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
                