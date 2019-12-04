from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, UserFollowingBridge


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'date_joined', 'bio', 'website')
    exclude = ('first_name', 'last_name', 'groups', 'user_permissions', 'email_confirmed')

    class Meta:
        model = User


class UserFollowingBridgeModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'date_followed')

    class Meta:
        model = UserFollowingBridge


admin.site.register(User, UserModelAdmin)
admin.site.register(UserFollowingBridge, UserFollowingBridgeModelAdmin)

admin.site.unregister(Group)
