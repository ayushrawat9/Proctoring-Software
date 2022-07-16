from django.contrib import admin
from .models import *
from django.contrib.admin.filters import AllValuesFieldListFilter


class DropdownFilter(AllValuesFieldListFilter):
    template = 'admin/dropdown_filter.html'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_filter = (('verified', DropdownFilter), ('role', DropdownFilter))
    search_fields = (
        'username',
    )
    fields = ['username', 'first_name', 'last_name', 'role', 'email', 'password', 'verified', 'image_tag',
              'user_permissions', 'is_staff']
    readonly_fields = ['image_tag']
