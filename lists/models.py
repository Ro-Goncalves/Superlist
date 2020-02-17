from django.db import models

# Create your models here.
class List(models.Model):
    #id = models.IntegerField(primary_key=True)
    pass

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List
                             ,default=None
                             ,null=True
                             ,blank=True)
    