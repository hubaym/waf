from time import timezone
import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlquote


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = datetime.datetime.now
        
        if not email:
            raise ValueError('The given email must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        print ('email %s, password %s' % (email,password))
        return self._create_user(email, password, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, **extra_fields)
    
    

class CustomUser(AbstractBaseUser):
    username    = models.CharField(max_length=254, unique=True)
    email       = models.EmailField(blank=True, unique=True)
    email_subs  = models.EmailField(blank=True, unique=True)
    language    = models.CharField(max_length=10, blank=True)
    facebook_id = models.BigIntegerField(blank=True, default = 0)

    date_joined  = models.DateTimeField(_('date joined'),default=datetime.datetime.now)
    #last_login   = models.DateTimeField(_('last login'))
    is_active    = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')    
    
    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)
        
    def get_short_name(self):
        "Returns the short name for the user."
        return self.email
    def get_full_name(self):
        "Returns the short name for the user."
        return self.email
    def get_username(self):
        "Returns the username for the user."
        return self.username
    def get_email_reg(self):
        "Returns the registrated email for the user."
        return self.email
    
    def get_email_subs(self):
        "Returns the subscripted email for the user."
        return self.email_subs

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])    
