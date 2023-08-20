from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
import json

from .models import User, Post, Comment


def pagination(request, objects_list):
    # pagination to show 10 objects (posts) per page
    paginator = Paginator(objects_list, 10)
    # get requested page number from url param
    page_number = request.GET.get('page') 
    # get page object for this page requested 
    page = paginator.get_page(page_number) 
    # return it
    return page


def index(request):
    param_all = request.GET.get("all")
    # get all posts in reverse chronological order
    all_posts = Post.objects.order_by("-date_posted").all()
    
    return render(request, "network/index.html", context={
        'page': pagination(request, all_posts),
        # when clicking 'All Posts' go to index page (where all posts displayed) but remove create post div even if user is logged in
        'creation_available': False if param_all else True,
    })


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


@login_required
def create(request):
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            new_post = Post(content=content, author=request.user)
            new_post.save()
            messages.success(request, 'Post created successfully!')
        else:
            messages.error(request, 'Invalid content.')

    # eventually redirect to homepage in case of success or failure of post creation (even in case of GET method)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    profile_user_posts = profile_user.user_posts.order_by("-date_posted").all()

    return render(request, "network/profile.html", context={
        'following': profile_user.following.all(),
        'followers': profile_user.followers.all(),
        'page': pagination(request, profile_user_posts),
        'profile_user': profile_user,
    })


@login_required
def follow_unfollow(request, user_id, action):
    profile_user = User.objects.get(pk=user_id)
    current_user = request.user
    if action == 'follow':
        profile_user.followers.add(current_user)
    # otherwise action == 'unfollow'
    else:
        profile_user.followers.remove(current_user)

    # # redirect to user profile page (same page) using the arg 'user_id'
    # return HttpResponseRedirect(reverse('profile', args=[user_id]))

    # alternatively: referring URL is the URL of the page that made the request (profile page)
    referring_URL = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(referring_URL)


@login_required
def following(request):
    current_user = request.user
    followed_users = current_user.following.all()
    # 'author__in' in Django is used to filter querysets based on a list of values (like list of authors instead of passing one author)
    followed_users_posts = Post.objects.filter(author__in=followed_users).order_by("-date_posted").all()
    
    return render(request, "network/following.html", context={
        'page': pagination(request, followed_users_posts),
    })


@login_required
def edit_post(request, post_id):
    # only PUT method is required
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)  # Bad request
    # in case its PUT method
    try:
        # get this post in a way that its not possible for a user, via any route, to edit another user’s posts
        this_post = Post.objects.get(author=request.user, pk=post_id)
    except Post.DoesNotExist:
        # here this_post is None
        return JsonResponse({"error": "Post not found."}, status=404)  # Not Found
    else:
        put_data = json.loads(request.body)
        new_content = put_data.get("content")
        
        # only if new content is valid and not empty and is different from old content then update it
        if new_content and new_content != this_post.content:
            this_post.content = new_content
            this_post.edited = True
            this_post.save()
            # alternatively HttpResponse(status=204) means a success response with no content
            return JsonResponse({"success": "This post was updated successfully."}, status=200)  # Success 
        # otherwise invalid new content
        return JsonResponse({"error": "Invalid new content."}, status=400)  # Bad request      
            

@login_required
def post_reaction(request, post_id):
    # only PUT method is required
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)  # Bad request
    # in case its PUT method
    try:
        # get this post
        this_post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        # here this_post is None
        return JsonResponse({"error": "Post not found."}, status=404)  # Not Found
    else:
        put_data = json.loads(request.body)
        reaction = put_data.get("reaction")
        # add current user to this post likers
        if reaction == 'like':
            this_post.likers.add(request.user)
        # remove current user from this post likers
        elif reaction == 'unlike':
            this_post.likers.remove(request.user)
        
        this_post.save()
        # alternatively HttpResponse(status=204) means a success response with no content
        return JsonResponse({"success": f"This post was {reaction}d successfully."}, status=200)  # Success