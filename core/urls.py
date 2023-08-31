from django.urls import path

from core.views import (
    CommentListAPIView,
    FollowersListAPIView,
    FollowingListAPIView,
    LikeCreateAPIView,
    LikeListAPIView,
    LikeRetrieveAPIView,
    PostCommentsListAPIView,
    PostCreateAPIView,
    PostDeleteAPIView,
    PostListAPIView,
    PostRetrieveAPIView,
    PostUpdateAPIView,
)

urlpatterns = [
    path("post/create/", PostCreateAPIView.as_view(), name="postcreate"),
    path("post/get/<uuid:pk>/", PostRetrieveAPIView.as_view(), name="postget"),
    path("post/list/", PostListAPIView.as_view(), name="postlist"),
    path("post/update/<uuid:pk>/", PostUpdateAPIView.as_view(), name="postupdate"),
    path("post/delete/<uuid:pk>/", PostDeleteAPIView.as_view(), name="postdelete"),
    path(
        "comments/post/<uuid:pk>/", PostCommentsListAPIView.as_view(), name="postdata"
    ),
    path("comments/user/<int:pk>/", CommentListAPIView.as_view(), name="commentuser"),
    path(
        "followers/user/<int:pk>/",
        FollowersListAPIView.as_view(),
        name="followers_of_user",
    ),
    path(
        "followings/user/<int:pk>/",
        FollowingListAPIView.as_view(),
        name="following_of_user",
    ),
    path("like/create/", LikeCreateAPIView.as_view(), name="likecreate"),
    path("like/get/<uuid:pk>/", LikeRetrieveAPIView.as_view(), name="likeget"),
    path("like/list/", LikeListAPIView.as_view(), name="likelist"),
]
