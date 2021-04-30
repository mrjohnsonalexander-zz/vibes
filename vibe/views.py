from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core import serializers
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token

from vibe.forms import ProfileForm, VibeForm, CommentForm

import json

from vibe.models import User, Vibe, Profile, Comment, Message


def index(request):
    # Authenticated users view vibes
    if request.user.is_authenticated:
        print('Getting vibes')
        vibes = Vibe.objects.all().order_by('-date_created')
        # Paginator
        paginator = Paginator(vibes, 10)
        page_number = request.GET.get('page')
        page_vibes = paginator.get_page(page_number)
        return render(request, "vibe/index.html", {
            'vibes': page_vibes
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
    Post, Put, and Get a vibe.
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
            body = json.loads(request.body.decode('utf-8'))
            vibe = Vibe.objects.prefetch_related('creator').get(pk=vibe_id)
            # Can only update vibes created
            if vibe.creator.username != request.user.username:
                return HttpResponse(
                    f"Login as {vibe.creator} to update vibe {vibe_id}",
                    status=401,
                )
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
            commentform = CommentForm()
            vibe_comments = Comment.objects \
                .prefetch_related('vibe') \
                .filter(vibe_id=vibe_id)
            return render(request, "vibe/index.html", {
                'vibe': vibe,
                'vibe_comments': vibe_comments,
                'commentform': commentform,
            })
        else:
            return render(request, "vibe/login.html", {
                "message": "Must login to post."
            })


def vibes(request):
    # Authenticated users view vibes
    if request.user.is_authenticated:
        vibes = Vibe.objects.prefetch_related('creator').all().order_by('-date_created')
        # Paginator
        paginator = Paginator(vibes, 10)
        page_number = request.GET.get('page')
        page_vibes = paginator.get_page(page_number)
        vibes_json = {}
        for i in range(len(page_vibes)):
            vibes_json[i] = {
                'id': page_vibes[i].id,
                'title': page_vibes[i].title,
                'description': page_vibes[i].description,
                'location': page_vibes[i].location,
                'creator': page_vibes[i].creator.username,
                'cheers': page_vibes[i].cheers,
                'date_created': page_vibes[i].date_created.strftime("%B %d,%Y, %I:%M %p"),
                'img_url': page_vibes[i].img_url,
            }
        return JsonResponse(vibes_json, safe=False)



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
    # /admin can manually create profile
    except Profile.DoesNotExist:
        profile = {'preferred_name': 'Contact admin to create profile'}
    return render(request, "vibe/index.html", {
        'profile': profile,
        'vibes': vibes,
        'self_profile': self_profile,
        'show_profile': True,
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
        'fans', 'follows').get(pk=profileid)
    if fan == 'True':
        profile.fans.remove(User.objects.get(
            username=request.user.username))
        print("removed profile fan")
    elif fan == 'False':
        profile.fans.add(User.objects.get(
            username=request.user.username))
        print("added profile fan")
    else:
        print("something went wrong")
    profile = Profile.objects.prefetch_related('user').get(pk=profileid)
    #return HttpResponseRedirect(reverse("vibe:profile" + '/' + profile.user.username))
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


def comments(request, vibe_id):
    """
    Create vibe comment.
    """
    if request.method == "POST":
        vibe = Vibe.objects.get(pk=vibe_id)
        commentform = CommentForm(request.POST)
        # Require user authentication
        if commentform.is_valid() and request.user.is_authenticated:
            # Save listing comment
            comment = commentform.save(commit=False)
            comment.vibe_id = vibe.pk
            comment.member = request.user
            comment.comment_date = datetime.now()
            comment.save()
            return HttpResponseRedirect(reverse(
                "vibe:vibe",
                kwargs={'vibe_id': vibe_id},
                ))
        else:
            return render(request, "vibe/login.html", {
                "message": "Must login to comment on vibe."
            })


@login_required
def messages(request, box):
    # Get current users profile
    profile = Profile.objects.get(user=request.user)
    # Filter message returned based on box
    if box == "received":
        messages = Message.objects.filter(
            recipients=profile, archived=False
        )
    elif box == "sent":
        messages = Message.objects.filter(
            sender=profile
        )
    elif box == "archived":
        messages = Message.objects.filter(
            recipients=profile, archived=True
        )
    else:
        return JsonResponse({"error": "Invalid box."}, status=400)

    # Return messages in reverse chronologial order
    try:
        messages = messages.order_by("-timestamp").all()
    except:
        print("no messages")
        #return JsonResponse({
        #   "error": f"No messages to returned for {box}"
        #}, status=400)
    #return JsonResponse([message.serialize() for message in messages], safe=False)
    return render(request, "vibe/index.html", {
        'box_messages': True,
        'messages': messages,
    })


@csrf_exempt
@login_required
def message(request, message_id):

    # Query for requested message
    try:
        message = Message.objects.get(pk=message_id)
    except Message.DoesNotExist:
        return JsonResponse({"error": "Message not found."}, status=404)

    # Return message contents
    if request.method == "GET":
        return JsonResponse(message.serialize())

    # Update whether message is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("read") is not None:
            message.read = data["read"]
        if data.get("archived") is not None:
            message.archived = data["archived"]
        message.save()
        return HttpResponse(status=204)

    # Message must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@csrf_exempt
@login_required
def compose(request):

    # Composing a new message must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient preferred_name
    data = json.loads(request.body)
    preferred_names = [preferred_name.strip() for preferred_name in data.get("recipients").split(",")]
    if preferred_names == [""]:
        return JsonResponse({
            "error": "At least one recipient required."
        }, status=400)

    # Convert preferred_name to profiles
    recipients = []
    for preferred_name in preferred_names:
        try:
            profile = Profile.objects.get(preferred_name=preferred_name)
            recipients.append(profile)
        except User.DoesNotExist:
            return JsonResponse({
                "error": f"Profile with preferred name {preferred_name} does not exist."
            }, status=400)

    # Get contents of message
    subject = data.get("subject", "")
    body = data.get("body", "")

    # Create one message for each recipient, plus sender
    profiles = set()
    self_profile = Profile.objects.get(user=request.user)
    profiles.add(profile)
    profiles.update(recipients)
    for profile in profiles:
        message = Message(
            sender=self_profile,
            subject=subject,
            body=body,
            read=self_profile == profile
        )
        message.save()
        for recipient in recipients:
            message.recipients.add(recipient)
        message.save()

    return JsonResponse({"message": "Message sent successfully."}, status=201)
