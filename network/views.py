from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json


from .models import User, Post, Comment

# Run from network app folder
# npx tailwindcss -i static/network/input.css -o static/dist/output.css --watch


def index(request):
    return render(request, "network/index.html")


@csrf_exempt
@login_required
def send_post(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    
    post = Post(
        body=data['body'],
        user_id = request.user.id
    )
    post.save()
    
    return JsonResponse({"message": "Post sent successfully."}, status=201)

def get_all_posts(request):
    posts = Post.objects.all()

    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()
    
    return JsonResponse([post.serialize() for post in posts], safe=False)


def get_user_posts(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user)

    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()

    return JsonResponse([post.serialize() for post in posts], safe=False)


@login_required
def get_following_posts(request):
    user = request.user
    following = user.following.all()
    posts = Post.objects.filter(user__in=following)

    # Return posts in reverse chronological order
    posts = posts.order_by('-timestamp').all()

    return JsonResponse([post.serialize() for post in posts], safe=False)


def check_login(request):
    if request.user.is_authenticated:
        return JsonResponse({'is_authenticated': True})
    else:
        return JsonResponse({'is_authenticated': False})

@login_required
def follow(request, user_id):
    user_to_follow = User.objects.get(id=user_id)
    if user_to_follow == request.user:
        # The user is trying to follow themselves
        return JsonResponse({'message': 'You cannot follow yourself'})

    if request.user.following.filter(id=user_to_follow.id).exists():
        # The user is already following the target user
        return JsonResponse({'message': 'You are already following this user'})

    request.user.following.add(user_to_follow)
    return JsonResponse({'message': 'User followed successfully'})


@login_required
def unfollow(request, user_id):
    user_to_unfollow = User.objects.get(id=user_id)
    if user_to_unfollow == request.user:
        # The user is trying to unfollow themselves
        return JsonResponse({'message': 'You cannot unfollow yourself'})

    if not request.user.following.filter(id=user_to_unfollow.id).exists():
        # The user is not currently following the target user
        return JsonResponse({'message': 'You are not currently following this user'})

    request.user.following.remove(user_to_unfollow)
    return JsonResponse({'message': 'User unfollowed successfully'})



@login_required
def get_follow_counts(request, user_id):
    user = User.objects.get(id=user_id)
    follower_count = user.followers.count()
    following_count = user.following.count()
    return JsonResponse({'follower_count': follower_count, 'following_count': following_count})



@login_required
def is_following(request, user_id):
    user_to_check = get_object_or_404(User, id=user_id)
    current_user = request.user
    
    if user_to_check == request.user:
        # The user is trying to follow themselves
        return JsonResponse({'message': 'You cannot follow yourself'})

    is_following = current_user.following.filter(id=user_to_check.id).exists()

    response_data = {
        'is_following': is_following,
    }

    return JsonResponse(response_data)



@login_required
def liked_posts(request):
    liked_posts = request.user.liked_posts.all()
    liked_post_ids = [post.id for post in liked_posts]
    return JsonResponse({'liked_posts': liked_post_ids})


@csrf_exempt
@login_required
def add_like(request, post_id):
    # Retrieve the Post object with the specified ID
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the current user has already liked the post
    if request.user in post.likes.all():
        # User has already liked the post, return an error response
        return JsonResponse({'message': 'User has already liked this post.'}, status=400)
    
    # Add the user to the post's list of likes and save the post
    if request.user.is_authenticated and request.user not in post.likes.all():
        post.likes.add(request.user)
        post.save()
    
    likes_count = post.likes.count()
    return JsonResponse({'likes': likes_count})


@csrf_exempt
@login_required
def remove_like(request, post_id):
    # Retrieve the Post object with the specified ID
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the current user has already liked the post
    if request.user not in post.likes.all():
        # User has not liked the post, return an error response
        return JsonResponse({'message': 'User has not liked this post.'}, status=400)
    
    # Remove the user from the post's list of likes and save the post
    if request.user.is_authenticated and request.user in post.likes.all():
        post.likes.remove(request.user)
        post.save()
    
    likes_count = post.likes.count()
    return JsonResponse({'likes': likes_count})

    



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
