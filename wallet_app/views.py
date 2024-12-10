from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Wallet, Transaction
#APIView
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from .service import generate_private_key
# Create your views here.
def home(request):
    return render(request, 'home.html')

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        #user = authenticate(username=username, password=password)
        user =User.objects.get(username=username)
        if user:
            return Response({'message': 'Login successfull'})
        return Response({'message': 'Login failed'})


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        return Response({'message': 'Login successfull'})
    return Response({'message': 'Login failed'})

#Wallet.objects.create(nom='wallet1', address='address1', private_key='private')

@api_view(['POST'])
def create_wallet(request):
    nom = request.data.get('nom') 
    address = request.data.get('address') 
    user = request.data.get('id')
    
    user  = User.objects.get(id=user)
    private_key , public_key = generate_private_key(user)
    wallet = Wallet.objects.create(nom=nom, address=address, private_key=private_key, public_key=public_key, user=user)
    str_private_key = str(private_key)
    str_public_key = str(public_key)
    return Response({'message': 'Wallet created successfully',"private_key":str_private_key, "public_key":str_public_key})