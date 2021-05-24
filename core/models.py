from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    typeName = models.CharField(default='receiver', max_length=50)


class DonatorInfo(models.Model):
    donator = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True)
    blood_group = models.CharField(max_length=2, default='')
    information = models.TextField()
    donate_amount = models.CharField(max_length=10, default='')


class Order(models.Model):
    donator = models.ForeignKey(
        DonatorInfo, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
