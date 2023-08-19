
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/create", views.create, name="create"),    
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/<int:user_id>/<str:action>", views.follow_unfollow, name="follow_unfollow"),
    path("following", views.following, name="following"),
    path("posts/edit/<int:post_id>", views.edit_post, name="edit_post"),
    
]
