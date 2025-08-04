from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
import uuid
from .usermanager import CustomBaseUserManager
# Create your models here.
class CustomUser(AbstractBaseUser,PermissionsMixin):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    phone_number=models.CharField(max_length=20,null=False,blank=False,unique=True)
    full_name=models.CharField(max_length=128,null=False,blank=False)
    email=models.EmailField(null=False,blank=False,unique=True)
    password=models.CharField(max_length=128,blank=False,null=False)
    profile_picture=models.ImageField(upload_to='static/profiles/',null=True,blank=True)
    is_driver=models.BooleanField(default=False)
    is_rider=models.BooleanField(default=True)
    is_active=models.BooleanField(default=True)
    last_login=models.DateTimeField(null=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    is_verified=models.BooleanField(default=False)
    is_online=models.BooleanField(default=False)
    objects=CustomBaseUserManager()
    is_staff=models.BooleanField(default=True)
    USERNAME_FIELD='email'
