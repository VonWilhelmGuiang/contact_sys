from django.db import models


class Account(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    active = models.BooleanField(null=True)


class Contact(models.Model):
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=25)
    company = models.CharField(max_length=50)
    email = models.CharField(max_length=100, unique=True)
