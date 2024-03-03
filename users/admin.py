from django.contrib import admin

from users.models import User

# Register your models here.

admin.site.register(User)


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)
