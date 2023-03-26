from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField()
    city = models.CharField(max_length=20)


class Winners(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField()
    city = models.CharField(max_length=20)
    win_summ = models.IntegerField()

# Create your models here.
