from django.db import models
from django.contrib.auth.models import AbstractUser
from cpf_field.models import CPFField

class User(AbstractUser):
    name = models.Charfield(max_length = 250)
    cpf = CPFField(max_length = 11)    

class Donator(models.Model):
    pass

class Nurce(models.Model):
    pass

class Adress(models.Model):
    pass

class Phone(models.Model):
    pass

class Allergies(models.Model):
    pass

class Donation(models.Model):
    pass

class Tubes(models.Model):
    pass

class CollectionBags(models.Model):
    pass

class Exames(models.Model):
    pass