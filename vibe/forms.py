from django.forms import ModelForm
from django.db import models
from django import forms

from vibe.models import Profile, Vibe


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'preferred_name']


class VibeForm(ModelForm):
    class Meta:
        model = Vibe
        fields = ['title', 'creator', 'description', 'location', 'img_url']
