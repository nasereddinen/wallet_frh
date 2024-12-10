from django.db import models
#import user
from django.contrib.auth.models import User

# Create your models here.
class Wallet(models.Model):
    nom  = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    private_key = models.CharField(max_length=200, blank=True, null=True)
    public_key = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallet")
    
    def __str__(self):
        return f'{self.nom} " " {self.address}'
    

    
class Transaction(models.Model):
    choice = (
        ('PENDING', 'PENDING'),
        ('COMPLETED', 'COMPLETED'),
        ('FAILED', 'FAILED')
    )
    date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="receiver")
    amount = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=choice, default='PENDING')
    
    def __str__(self):
        return f'{self.sender.nom} " " {self.receiver.nom} " " {self.amount}'