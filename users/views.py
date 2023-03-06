from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.core import serializers
from .serializers import UserSerializer
from .serializers import AirportSerializer
from .models import User, Airports
import jwt, datetime

class AirportcreateView(APIView):
    def post(self,request):
        token = request.headers.get("bearer")

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        request.data["createdBy"] = serializer.data['email']

        serializerAirport = AirportSerializer(data=request.data)
        serializerAirport.is_valid(raise_exception=True)
        serializerAirport.save()
        return Response(serializerAirport.data)

class AirportsView(APIView):
    def get(self,request):   
        token = request.headers.get("bearer")  
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')   

        results = Airports.objects.all()
        data = AirportSerializer(results,many=True)

        resp = data.data

        return Response(resp)    


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        payload_refresh = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
        'iat': datetime.datetime.utcnow()
        }

        refresh_token =  jwt.encode(payload_refresh, 'refresh_secret', algorithm='HS256')

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.data = {
            'jwt': token,
            "refresh_token":refresh_token
        }
        return response


class UserView(APIView):

    def get(self, request):
        token = request.headers.get('bearer')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RefreshTokenView(APIView):
    def post(self, request):
        token = request.data['refresh_token']

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'refresh_secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')  

        user = User.objects.filter(id=payload['id']).first()
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.data = {
            'jwt': token,
        }
        return response   