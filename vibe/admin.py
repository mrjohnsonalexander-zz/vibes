from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from vibe.models import User, Vibe, Comment, Profile, Message


class VibeUserAdmin(UserAdmin):
    model = User


# Register models
admin.site.register(User, VibeUserAdmin)
admin.site.register(Vibe)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Message)