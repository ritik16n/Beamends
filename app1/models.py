from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.contrib.sites.models import Site

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class Link(models.Model):
    user=models.ForeignKey(User,default=0)
    date=models.DateField(default=datetime.date.today())
    item=models.CharField(max_length=20)
    description=models.TextField(max_length=200,blank=True)
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(default=0,max_digits=10,decimal_places=2)
    total=models.DecimalField(max_digits=100,decimal_places=2)
    sites = models.ManyToManyField(Site)

    def __str__(self):
        return self.item
