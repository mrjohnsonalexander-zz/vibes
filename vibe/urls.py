from django.urls import path

from . import views

app_name = 'vibe'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("vibe", views.vibe, name="vibe"),
    path("vibes", views.vibes, name="vibes"),
    path("vibe/<str:vibe_id>", views.vibe, name="vibe"),
    path("vibe_details/<str:vibe_id>",
         views.vibe_details,
         name="vibe_details"),
    path("cheers/<str:vibe_id>", views.cheers, name="cheers"),
    path("comments/<int:vibe_id>/", views.comments, name="comments"),
    path("fan/<int:profileid>/<str:fan>", views.fan, name="fan"),
    path("message/<int:message_id>", views.message, name="message"),
    path("messages/<str:box>", views.messages, name="messages"),
    path("message", views.compose, name="compose"),
]
