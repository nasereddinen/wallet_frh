from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User

from .serializers import WalletSerializer
from .models import Wallet, Transaction
#APIView
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

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

def generate_wallet_addresse(user_id):
    wallet_add = f"wallet_{user_id}_xxxx"
    return wallet_add

@api_view(['POST'])
def login(request):
    
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        private_key , public_key = generate_private_key(user)
        address = generate_wallet_addresse(user.id)
        wallet, created = Wallet.objects.get_or_create(
            user=user,
            defaults={
                'nom': user.username,
                'address': address,
                'private_key': private_key,
                'public_key': public_key
            }
        )        
        
        str_private_key = str(private_key)
        str_public_key = str(public_key)
        
        return Response({'message': 'Login successfull', 'token': token.key})
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

@api_view(['POST'])
def get_wallet(request):
    token = request.data.get('token')
    user_id = Token.objects.get(key=token).user_id
    user = User.objects.get(id=user_id)
    wallet = Wallet.objects.get(user=user_id)
    wallet_data = WalletSerializer(wallet, many=False).data
    return Response({'message': 'Wallet found', 'wallet': wallet_data})

@api_view(['POST'])
def transfer(request):
    sender = request.data.get('sender')
    receiver = request.data.get('receiver')
    amount = request.data.get('amount')
    
    sender = Wallet.objects.get(id=sender)
    receiver = Wallet.objects.get(id=receiver)
    
    if sender and receiver:
        if sender.user == receiver.user:
            return Response({'message': 'You cannot transfer to yourself'})
        if sender.amount < amount:
            return Response({'message': 'Insufficient funds'})
        
        sender.amount -= amount
        receiver.amount += amount
        sender.save()
        receiver.save()
        
        Transaction.objects.create(sender=sender, receiver=receiver, amount=amount)
        return Response({'message': 'Transfer successfull'})
    return Response({'message': 'Transfer failed'})