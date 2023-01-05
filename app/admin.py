from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'facebook_id', 'facebook_name', 'email']


admin.site.register(User, UserAdmin)
