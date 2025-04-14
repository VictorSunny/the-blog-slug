from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as lazytext
from django_countries.fields import CountryField

# Create your models here.

class SlugManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(lazytext("Please provide a valid email address"))
        
        email = self.normalize_email(email)
        new_user = self.model(email= email, **extra_fields)
        new_user.set_password(password)
        new_user.is_active = True
        new_user.save()

        return new_user
    
    #set necessary permissions for superuser
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(lazytext("Superuser should have is_staff set to True"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(lazytext("Superuser should have is_superuser set to True"))
        if extra_fields.get('is_active') is not True:
            raise ValueError(lazytext("Superuser should have is_active set to True"))
        
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    email = models.EmailField(max_length= 100, unique= True)
    username = models.CharField(max_length= 20, unique= True)
    first_name = models.CharField(max_length= 25)
    last_name = models.CharField(max_length= 25)
    about = models.CharField(max_length= 755, default= 'Happy to be here!', blank= True)
    nationality = CountryField(blank_label= "what's your nationality?")
    followers = models.ManyToManyField('self', symmetrical= False, related_name= 'following', blank= True)
    personalized_articles = models.JSONField(blank= True, null= True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username' ,'first_name', 'last_name']

    objects = SlugManager()

    def __str__(self) -> str:
        return self.username

class OTPVerification(models.Model):
    email = models.EmailField(max_length= 100, unique= True)
    code = models.CharField(blank= True, max_length= 6)
    created_at = models.DateTimeField(auto_now= True)