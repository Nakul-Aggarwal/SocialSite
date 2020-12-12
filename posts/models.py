from django.db import models
from django.conf import settings
from django.urls import reverse

# pip install misaka
import misaka

from groups.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    group = models.ForeignKey(Group, related_name="posts",null=True, blank=True,on_delete=models.CASCADE)
    picture = models.ImageField(upload_to = 'posts', blank=True)

    def __str__(self):
        return self.message

    def get_absolute_url(self):
        return reverse(
            "posts:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]

class Comment(models.Model):
    post = models.ForeignKey('posts.Post', related_name='comments',on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="authors",on_delete=models.CASCADE)
    text = models.TextField()
    picture = models.ImageField(upload_to = 'comments', blank=True)
    created_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text
