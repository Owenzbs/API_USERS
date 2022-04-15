from django.forms import ValidationError
from django.shortcuts import render
from itsdangerous import Serializer
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import *
import jwt, datetime
from django.core import mail
from django.conf import settings
# Create your views here.



class RegisterView(APIView):
    def post(self, request):
        first_name_req=request.data["first_name"]
        if first_name_req.isalpha() is False:
            return Response(ValidationError("Your first_name should have only letters"))
        last_name_req=request.data["last_name"]
        if last_name_req.isalpha() is False:
            return Response(ValidationError("Your last_name should have only letters"))
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        return Response(serializer.data)
            
class LoginView(APIView):
    def post(self, request):
        email=request.data['email']
        password=request.data['password']
        
        user=User.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        
        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        
        token=jwt.encode(payload, 'secret', algorithm="HS256")
        
        response=Response()
        
        response.set_cookie(key='jwt', value=token, httponly=True)
        
        response.data={
            "jwt":token
        }
        
        return response
    

class UserView(APIView):
    def get(self, request, **kwargs):
        user_id=kwargs.get('id', None)
        user=User.objects.filter(pk=user_id).first()
        
        if user is None:
            return Response({
            "Message":"User with this id doesn't exists!"
        })
            
        return Response({
            "id":user.id,
            "first_name":user.first_name,
            "last_name":user.last_name,
            "email":user.email,
            "password":user.password,
            
        })
    
    def put(self, request, *args,**kwargs):
        pk=kwargs.get("id")
        if not pk:
            return Response({"error":"Method PUT is not allowed!"})

        try:
            instance=User.objects.get(pk=pk)
        except:
            return Response({"error":"Object does'n exists!"})
        
        first_name_req=request.data["first_name"]
        if first_name_req.isalpha() is False:
            return Response(ValidationError("Your first_name should have only letters"))
        last_name_req=request.data["last_name"]
        if last_name_req.isalpha() is False:
            return Response(ValidationError("Your last_name should have only letters"))
        serializer=UserSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        connection = mail.get_connection()
        connection.open()
        email = mail.EmailMessage(
            "Notification",
            "YOUR UPDATE SUCCESS!!!!!",
            settings.EMAIL_HOST_USER,
            [serializer.data['email']],
        )
        email.fail_silently=False
        email.send()
        connection.close()
        return Response({"updated": serializer.data})
 
