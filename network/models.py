from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # 'symmetrical=False' arg indicates relationship is not symmetric, means if User A follows User B, it don't imply that User B follows User A
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, null=True, related_name='following')


class Post(models.Model):
    content = models.TextField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)    # automatically populated with current date
    edited = models.BooleanField(default=False)
    edited_on = models.DateTimeField(auto_now=True)    # automatically populated with current date on every update of instance    
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_posts")
    likers = models.ManyToManyField(User, blank=True, null=True, related_name="liked_posts")

    def __str__(self):
        return f'"{self.content}" -- (posted on {self.date_posted.strftime("%b. %d, %Y, %I:%M %p")} by {self.author})'
    

class Comment(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True, null=True)    # automatically populated with current date
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name="post_comments")

    def __str__(self):
        return f'{self.author.username}: "{self.text}" -- (post: "{self.post.content}")'
