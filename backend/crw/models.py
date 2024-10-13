from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=10)
    userid = models.CharField(max_length=20, unique=True)
    birth = models.DateField()
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=30,default='')
    phone = models.IntegerField()


    REQUIRED_FIELDS = ['email','birth','phone']
    USERNAME_FIELD = 'userid' 

    class Meta:
        app_label = 'crw'

    def __str__(self):
        return self.userid


class dict(models.Model):
    class Meta :
        db_table = 'dict'
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=70, blank=True)
    description = models.TextField(blank=True)
    description2 = models.TextField(blank=True)
    original_word = models.TextField(blank=True)
    korean_word = models.TextField(blank=True)
    synonym = models.TextField(blank=True)
    translations = models.TextField(blank=True)
    word_level = models.IntegerField()

class Search_list(models.Model):
    class Meta :
        db_table = 'Search_list'
    id = models.IntegerField(primary_key=True)
    search_word = models.CharField(max_length=70, blank=True)
    search_pos = models.CharField(max_length=70, blank=True)