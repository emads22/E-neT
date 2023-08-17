
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),   
    path("login", views.login_view, name="login"),    
    # path("login/error", views.login_first, name="login_first"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/create", views.create, name="create"),
    path("posts/", views.index, name="all_posts"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    # path("posts/<int:post_id>", views.post, name="post"),
    path("profile/<int:user_id>/<str:action>", views.follow_unfollow, name="follow_unfollow"),
    
]
