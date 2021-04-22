from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import json

from datetime import datetime

from .forms import ProfileForm, VibeForm

from .models import User, Vibe

from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.contrib.auth.decorators import login_required

def index(request):
    # Authenticated users view vibes
    if request.user.is_authenticated:
        print('Getting vibe')
        vibes = Vibe.objects.all().order_by('-date_created')
        return render(request, "vibe/index.html", {
            'vibes': vibes
        })
    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("vibe:login"))


def login_view(request):
    """
    Render login page
    """
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("vibe:index"))
        else:
            return render(request, "vibe/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "vibe/login.html")


def logout_view(request):
    """
    Render log out page
    """
    logout(request)
    return HttpResponseRedirect(reverse("vibe:index"))


def register(request):
    """
    Render Registration Page
    """
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "vibe/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "vibe/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("vibe:index"))
    else:
        return render(request, "vibe/register.html")


def profile(request, username):
    # Create post
    if request.method == "POST":
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid() and request.user.is_authenticated:
            print('Creating profile')
            profile = profile_form.save(commit=False)
            profile.creator = request.user
            profile.save()
            return HttpResponseRedirect(reverse("vibe:profile" + username))
    # TODO: GET profile date
    profile = "testprofile"
    return render(request, "vibe/profile.html", {
        'profile': profile,
    })


@requires_csrf_token
def vibe(request):
    """
    Post, Put, and Get vibes
    """
    print("Vibing")
    if request.method == "POST":
        # vibe.js vibeForm
        body = json.loads(request.body.decode('utf-8'))
        vibe_data = {
           'title': body['title'],
           'creator': request.user,
           'description': body['description'],
           'location': body['location'],
           'img_url': body['img_url'],
        }
        vibeform = VibeForm(vibe_data)
        if vibeform.is_valid() and request.user.is_authenticated:
            vibe = vibeform.save(commit=False)
            vibe.date_created = datetime.now()
            vibe.save()
            return HttpResponse(status=200)
        else:
            return render(request, "vibe/login.html", {
                "message": "Must login to post."
            })
    elif request.method == "PUT":
        if request.user.is_authenticated:
            print('Updating vibe')
            vibe = request.PUT
            print(vibe)
            return HttpResponseRedirect(reverse("vibe:index"))
        else:
            return render(request, "vibe/login.html", {
                "message": "Must login to post."
            })
    # Assume GET request
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("vibe:index"))
        else:
            return render(request, "vibe/login.html", {
                "message": "Must login to post."
            })

def vibe_details(request, vibe_id):
    vibe = Vibe.object.get(pk=vibe_id)
    return render(request, "vibe/index.html", {
        "vibe": vibe
        })