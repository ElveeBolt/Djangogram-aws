from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminOriginal
from .models import User, UserFriend


# Register your models here.
class UserAdmin(UserAdminOriginal):
    model = User
    list_display = ['username', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']

    add_fieldsets = (
        *UserAdminOriginal.add_fieldsets,
        (
            'Main info',
            {
                'fields': ['avatar', 'bio']
            }
        )
    )

    fieldsets = (
        *UserAdminOriginal.fieldsets,
        (
            'Main info',
            {
                'fields': ['avatar', 'bio']
            }
        )
    )


class UserFriendAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'date_created']


admin.site.register(User, UserAdmin)
admin.site.register(UserFriend, UserFriendAdmin)
