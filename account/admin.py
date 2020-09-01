from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth.admin import UserAdmin as ModelAdmin


# Register your models here.


class UserAdmin(ModelAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('username', 'created_at', 'updated_at', )
    list_filter = ('admin',)
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('id', 'username', 'password', 'task_count')}),
        ('Personal Info', {'fields': ('email', 'first_name', 'last_name', )}),
        ('Permissions', {'fields': ('admin', 'active', 'staff', 'authenticated', 'anonymous')})
    )


admin.site.register(User, UserAdmin)

admin.site.unregister(Group)

