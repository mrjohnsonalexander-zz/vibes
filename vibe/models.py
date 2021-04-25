from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    preferred_name = models.CharField(max_length=80)
    user = models.OneToOneField(
        User,
        related_name='user',
        on_delete=models.CASCADE,
        null=True,
        blank=False)
    fans = models.ManyToManyField(
        User,
        related_name='fans',
        blank=True)
    follows = models.ManyToManyField(
        User,
        related_name='follows',
        blank=True)


class Vibe(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=180, blank=True)
    description = models.TextField()
    location = models.TextField()
    date_created = models.DateTimeField(
        auto_created=True, null=False, blank=False)
    img_url = models.URLField(null=True, blank=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='creator')
    cheers = models.BigIntegerField(default=0)
    user_cheers = models.ManyToManyField(
        User,
        related_name='user_cheers',
        blank=True)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    vibe = models.ForeignKey(
        Vibe,
        on_delete=models.CASCADE,
        db_column='listing_id',
        blank=True,
        null=True)
    comment = models.CharField(max_length=180)
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='member')
    comment_date = models.DateTimeField(auto_created=True)
