from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token

from vibe.forms import ProfileForm, VibeForm

import json

from vibe.models import User, Vibe, Profile


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
        # Attempt to create new user and profile
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile(preferred_name=username, user=user)
            profile.save()
        except IntegrityError:
            return render(request, "vibe/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("vibe:index"))
    else:
        return render(request, "vibe/register.html")


@requires_csrf_token
def vibe(request, vibe_id=None):
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
            body = json.loads(request.body.decode('utf-8'))
            vibe = Vibe.objects.prefetch_related('creator').get(pk=vibe_id)
            # Can only update vibes created
            if vibe.creator.username != request.user.username:
                print("Unauthorized editing was prevented")
                return HttpResponse(f"Must login as {vibe.creator} to update vibe {vibe_id}", status=401)
            vibe.title = body['title']
            vibe.description = body['description']
            vibe.location = body['location']
            vibe.img_url = body['img_url']
            vibe.save(update_fields=[
                'title',
                'description',
                'location',
                'img_url'
            ])
            return HttpResponseRedirect(reverse("vibe:index"))
        else:
            return render(request, "vibe/login.html", {
                "message": "Must login to post."
            })
    # Assume GET request
    else:
        if request.user.is_authenticated:
            vibe = Vibe.objects.get(pk=vibe_id)
            return render(request, "vibe/index.html", {
                'vibe': vibe
            })
        else:
            return render(request, "vibe/login.html", {
                "message": "Must login to post."
            })


def vibe_details(request, vibe_id):
    vibe = Vibe.objects.prefetch_related('creator').get(pk=vibe_id)
    vibe_json = {
        'id': vibe.pk,
        'title': vibe.title,
        'description': vibe.description,
        'location': vibe.location,
        'creator': vibe.creator.username,
        'cheers': vibe.cheers,
        'date_created': vibe.date_created.strftime("%B %d,%Y, %I:%M %p"),
        'img_url': vibe.img_url,
    }
    return JsonResponse(vibe_json, safe=False)


def profile(request, username):
    # Create post
    if request.method == "POST":
        profileForm = ProfileForm(request.POST)
        if profileForm.is_valid() and request.user.is_authenticated:
            print('Creating Post')
            profile = profileForm.save(commit=False)
            profile.author = request.user
            profile.save()
            return HttpResponseRedirect(reverse("vibe:index" + username))
    # Hide Follow/Unfollow button on users own profile
    self_profile = False
    if request.user.username == username:
        self_profile = True
    # Show by all user's vibes
    vibes = Vibe.objects.filter(
        creator=User.objects.get(username=username)).order_by('-date_created')
    paginator = Paginator(vibes, 1)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    # Get clicked Profile
    fan = False
    fan_count = 0
    follow_count = 0
    try:
        # Set profile button to Follow or Unfollow
        profile = Profile.objects.prefetch_related(
            'user', 'fans', 'follows').get(
                user=User.objects.get(username=username))
        fans = profile._prefetched_objects_cache['fans']
        for fan in fans:
            if fan.username == request.user.username:
                fan = True
                break
        fan_count = len(profile._prefetched_objects_cache['fans'])
        follow_count = len(profile._prefetched_objects_cache['follows'])
    # /admin manually create profile to enable following
    except Profile.DoesNotExist:
        profile = {'preferred_name': 'Contact admin to create profile'}
    return render(request, "vibe/index.html", {
        'profile': profile,
        'vibes': vibes,
        'self_profile': self_profile,
        'fan': fan,
        'fan_count': fan_count,
        'follow_count': follow_count
    })


@csrf_exempt
@login_required
def fan(request, profileid, fan):
    """
    Update Profile's fan
    """
    print(f"Profile {profileid} has fan {request.user} {fan}")
    profile = Profile.objects.prefetch_related(
        'fan', 'follows').get(pk=profileid)
    if fan == 'True':
        profile.fan.remove(User.objects.get(
            username=request.user.username))
        print("removed profile fan")
    elif fan == 'False':
        profile.fan.add(User.objects.get(
            username=request.user.username))
        print("added profile fan")
    else:
        print("something went wrong")
    return HttpResponseRedirect(reverse("vibe:index"))


@csrf_exempt
@login_required
def cheers(request, vibe_id):
    # Update vibe cheer users
    # Get current user's that cheered the vibe
    if request.method == "PUT":
        vibe = Vibe.objects.prefetch_related('user_cheers').get(pk=vibe_id)
        user_cheers = vibe._prefetched_objects_cache['user_cheers']
        # Add or Remove post like user
        user_cheers_vibe = False
        for user in user_cheers:
            if request.user == user:
                user_cheers_vibe = True
        if user_cheers_vibe:
            # add vibe.user_cheers and 1 vibe cheer
            vibe.user_cheers.remove(User.objects.get(
                username=request.user.username))
            vibe.cheers = vibe.cheers - 1
            print(f"User stopped cheering vibe {vibe_id}")
        else:
            # remove vibe.user_cheers and -1 from vibe.cheers
            vibe.user_cheers.add(User.objects.get(
                username=request.user.username))
            vibe.cheers = vibe.cheers + 1
            print(f"User cheers vibe {vibe_id}")
        vibe.save()
        return HttpResponse(status=200)
