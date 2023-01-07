from django.db import models
from AdminApp.models import UserInfo,Product
from datetime import datetime
# Create your models here.

class MyCart(models.Model):
    user = models.ForeignKey(to='AdminApp.UserInfo', 
              on_delete=models.CASCADE)
    cake = models.ForeignKey(to='AdminApp.Product', 
               on_delete=models.CASCADE)
    qty = models.IntegerField()

    class Meta:
        db_table  = "MyCart"



class OrderMaster(models.Model):
    user = models.ForeignKey(to='AdminApp.UserInfo', 
              on_delete=models.CASCADE)
    amount = models.FloatField(default=1000)
    dateOfOrder = models.DateTimeField(default=datetime.now)
    details = models.CharField(max_length=200)
    class Meta:
        db_table  = "OrderMaster"

class Checkout(models.Model):             
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6)
    phone = models.CharField(max_length=10)
   

    def __str__(self):
        return self.name
    class Meta:
        db_table  = "Checkout"

class Review(models.Model):  
    user=models.CharField(max_length=100)
    ratings=models.IntegerField(default=1)
    feedback=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    class Meta:
        db_table  = "Review"
             
