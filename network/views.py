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


# @login_required
def index(request):
    param_all = request.GET.get("all")
    # get all posts in reverse chronological order
    all_posts = Post.objects.order_by("-date_posted").all()
    
    return render(request, "network/index.html", context={
        'page': pagination(request, all_posts),
        # when clicking 'All Posts' go to index page (where all posts displayed) but remove create post div even if user is logged in
        'creation_available': False if param_all else True,
    })


# def all_posts(request):

#     # get all post of this user in reverse chronological order
#     all_posts = Post.objects.order_by("-date_posted").all()
#     # # pagination to show 10 objects (posts) per page
#     # paginator = Paginator(all_posts, 10)
#     # # get requested page number from url param
#     # page_number = request.GET.get('page') 
#     # # get page object for this page requested
#     # page = paginator.get_page(page_number)
    
#     return render(request, "network/posts.html", context={
#         # 'posts': all_posts,
#         'page': pagination(request, all_posts),
#     })

#     # # Filter emails returned based on mailbox
#     # posts = Post.objects.filter(author=request.user)
    
#     # # Return posts in reverse chronologial order
#     # posts = posts.order_by("-timestamp").all()
#     # return JsonResponse([post.serialize() for post in posts], safe=False)


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
    

# def login_first(request):
#     return render(request, "network/login.html", context= {
#         'login_first': True,
#     })


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
            # return redirect('post_list')  # Redirect to a post list view
        else:
            messages.error(request, 'Invalid content.')
            # return redirect('create_post')  # Redirect back to the create post view    
    # eventually redirect to homepage in case of success or failure of post creation (even in case of GET method)
    return HttpResponseRedirect(reverse('index'))

    # # Composing a new email must be via POST
    # # if request.method != "POST":
    # #     return JsonResponse({"error": "POST request required."}, status=400)


    # data = json.loads(request.body)
    
    # # Get content of post
    # content = data.get("content", "")

    # # Create a post
    # post = Post(
    #     content=content,
    #     author=request.user
    #     )
    
    # post.save()

    # return JsonResponse({"message": "Post added successfully."}, status=201)


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
def post(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(user=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post content
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update post
    elif request.method == "PUT":
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()
        return HttpResponse(status=204)

    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)