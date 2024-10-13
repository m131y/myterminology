from django.db import models

# Create your models here.

class Word(models.Model):
    class Meta :
        db_table = 'word'

    word = models.CharField(max_length=70, blank=True)
    word_type = models.CharField(max_length=70, blank=True)
    definition = models.TextField(blank=True)
    pos = models.CharField(max_length=70, blank=True)


class Result(models.Model):
    resultword = models.CharField(max_length=50)
    
    def __str__(self):
        return self.resultword
    