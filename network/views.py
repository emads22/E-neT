from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
import json

from .models import User, Post



# <==================================================<Helper Tools>==================================================>
def pagination(request, objects_list):
    # pagination to show 10 objects (posts) per page
    paginator = Paginator(objects_list, 10)
    # get requested page number from url param
    page_number = request.GET.get('page') 
    # get page object for this page requested 
    page = paginator.get_page(page_number) 
    # return it
    return page



# <==================================================<Views Functions>==================================================>
@login_required
def index(request):
    # get all posts in reverse chronological order
    all_posts = Post.objects.order_by("-date_posted").all()
    
    return render(request, "network/index.html", context={
        'page': pagination(request, all_posts),
        'heading': "Latest Posts",
    })


@login_required
def create(request):
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            new_post = Post(content=content, author=request.user)
            new_post.save()
            messages.success(request, 'Post created successfully!')
        else:
            messages.error(request, 'Invalid new content.')

    # eventually redirect to homepage in case of success or failure of post creation (even in case of GET method)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    profile_user_posts = profile_user.user_posts.order_by("-date_posted").all()

    return render(request, "network/profile.html", context={
        'page': pagination(request, profile_user_posts),
        'profile_user': profile_user,
        'following': profile_user.following.all(),
        'followers': profile_user.followers.all(),        
    })


@login_required
def follow_unfollow(request, user_id, action):
    profile_user = User.objects.get(pk=user_id)
    current_user = request.user
    if action == 'follow':
        profile_user.followers.add(current_user)
        action_message = "started"
    # otherwise action == 'unfollow'
    else:
        profile_user.followers.remove(current_user)
        action_message = "stopped"

    # # redirect to user profile page (same page) using the arg 'user_id'
    # return HttpResponseRedirect(reverse('profile', args=[user_id]))
    
    messages.success(request, f"You {action_message} following {profile_user.username.title()}")
    # alternatively: referring URL is the URL of the page that made the request (profile page)
    referring_URL = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(referring_URL)


@login_required
def following(request):
    current_user = request.user
    followed_users = current_user.following.all()
    # 'author__in' in Django is used to filter querysets based on a list of values (like list of authors instead of passing one author)
    followed_users_posts = Post.objects.filter(author__in=followed_users).order_by("-date_posted").all()
    
    return render(request, "network/index.html", context={
        'page': pagination(request, followed_users_posts),
        'heading': "Latest from Followed Profiles",
    })


@login_required
def edit_post(request, post_id):
    # only PUT method is required
    if request.method != "PUT":
        return JsonResponse({"message": ("danger", "PUT request required only.")}, status=400)  # Bad request
    # in case its PUT method
    try:
        # get this post in a way that its not possible for a user, via any route, to edit another user’s posts
        this_post = Post.objects.get(author=request.user, pk=post_id)
    except Post.DoesNotExist:
        # here this_post is None
        return JsonResponse({"message": ("danger", "Post not found.")}, status=404)  # Not Found
    else:
        put_data = json.loads(request.body)
        new_content = put_data.get("content")

        if new_content == this_post.content:
            return JsonResponse({"message": ("warning", "No changes occurred.")}, status=200)  # Success
        
        # only if new content is valid and not empty and is different from old content then update it
        elif new_content:
            this_post.content = new_content
            this_post.edited = True
            this_post.save()
            # alternatively HttpResponse(status=204) means a success response with no content
            return JsonResponse({
                "message": ("success", "Post updated successfully!"),
                "edited_content": new_content
                }, status=200)  # Success 
        
        # otherwise invalid new content
        return JsonResponse({"message": ("danger", "Invalid new content.")}, status=400)  # Bad request      
            

@login_required
def post_reaction(request, post_id):
    # only GET method is required
    if request.method != "GET":
        return JsonResponse({"message": ("danger", "GET request required only.")}, status=400)  # Bad request
    # in case its PUT method
    try:
        # get this post
        this_post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        # here this_post is None
        return JsonResponse({"message": ("danger", "Post not found.")}, status=404)  # Not Found
    else:
        # if current user is among the likers of this post then pressing like button will remove him from this post likers (unlike the post)
        if request.user in this_post.likers.all():
            this_post.likers.remove(request.user)
            reaction = "unlike"
        # otherwise add him to this post likers (like the post)
        else:
            this_post.likers.add(request.user)
            reaction = "like"
        
        this_post.save()
        # alternatively HttpResponse(status=204) means a success response with no content
        return JsonResponse({
            "message": ("success", f"You {reaction}d this post."),
            "total_likes": this_post.likers.count()
            }, status=200)  # Success
    


# <==================================================<Given Functions>==================================================>
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