import uuid

from django.db import models

# from django.contrib.auth.models import User
from authentication.models import User


class Post(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BaseLikeComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Like(BaseLikeComment):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        unique_together = (
            "user",
            "post",
        )

    def __str__(self):
        return str(self.user)


class Comment(BaseLikeComment):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user)


# class Follow(models.Model):
#     uuid = models.UUIDField(auto_created=True, primary_key=True)
#     follower = models.ManyToManyField(User, on_delete=models.CASCADE)


class Follow(models.Model):
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user")
    user_following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_following"
    )

    class Meta:
        unique_together = (
            "user",
            "user_following",
        )

    def __str__(self):
        return str(self.user)
