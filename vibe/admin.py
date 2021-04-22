from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Vibe, Comment


class VibeUserAdmin(UserAdmin):
    model = User


# Register models
admin.site.register(User, VibeUserAdmin)
admin.site.register(Vibe)
admin.site.register(Comment)