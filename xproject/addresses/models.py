from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Addresses(models.Model):
    name = models.CharField(max_length=10,default=False)
    userid = models.CharField(max_length=10,default=False)
    userpw = models.CharField(max_length=10,default=False)
    signup_confirmation = models.BooleanField(default=False)

    class Meta:
        db_table = 'addresses'

class Pictures(models.Model):
    #picture=models.ImageField(upload_to="image")
    userid = models.CharField(max_length=10,default=False)
    first_picture=models.ImageField(upload_to="image",default=False)
    second_picture=models.ImageField(upload_to="image",default=False)
    third_picture=models.ImageField(upload_to="image",default=False)

class LoginPicture(models.Model):
    userid = models.CharField(max_length=10,default=False)
    login_picture=models.ImageField(upload_to="login")
