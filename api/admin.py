from django.contrib import admin
from .models import CustomUser,FriendRequest
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(FriendRequest)
