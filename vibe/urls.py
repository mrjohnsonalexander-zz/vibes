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
]
