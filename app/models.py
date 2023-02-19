from django.db import models
from django.db.models import Model

class user_model(Model):
    wallet_address = models.CharField(max_length=50, primary_key=True)
    timer = models.CharField(max_length=25)
    claim = models.IntegerField()
    withdrawl = models.IntegerField()
    password = models.CharField(max_length=30)
