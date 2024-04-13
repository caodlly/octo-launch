from django.contrib import admin
from apps.users.models import User
# Register your models here.


@admin.register(User)
class UserModel(admin.ModelAdmin):
    list_display = ('username', 'email', 'name',
                    'last_login', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_per_page = 25
    date_hierarchy = 'last_login'
