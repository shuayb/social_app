from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'date_joined', 'bio', 'website')
    exclude = ('first_name', 'last_name', 'groups', 'user_permissions', 'email_confirmed')

    class Meta:
        model = User


admin.site.register(User, UserModelAdmin)
admin.site.unregister(Group)
