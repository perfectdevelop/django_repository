from django.contrib import admin

from .models import UserType, DonatorInfo, Order

admin.site.register(UserType)
admin.site.register(DonatorInfo)
admin.site.register(Order)
