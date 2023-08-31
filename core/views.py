from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# from core.CustomPagination import CustomPagination
from core.serializers import (
    CommentSerializer,
    FollowersSerializer,
    FollowingsSerializer,
    LikeSerializer,
    PostSerializer,
    PostCreateSerializer
)

from .models import Comment, Follow, Like, Post
from .permissions import IsAuthenticatedOwner


class PostCreateAPIView(CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if "user" not in request.data:
            request.data["user"] = request.user.id

        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"msg": "Post Created Successfully!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.filter(pk=pk).first()
        if post is not None:
            serilizer = PostSerializer(post)
            return Response(serilizer.data, status=status.HTTP_200_OK)
        return Response(
            {"errors": {"msg": "Invalid Post Id!"}},
            status=status.HTTP_400_BAD_REQUEST,
        )


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated]


class PostUpdateAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOwner]

    def put(self, request, pk, *args, **kwargs):
        if "user" not in request.data:
            request.data["user"] = request.user.id

        post = Post.objects.filter(pk=pk).first()
        if post is not None:
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {"msg": "Post Updated Successfully!"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"errors": {"msg": "Invalid Post Id!"}},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, pk, *args, **kwargs):
        if "user" not in request.data:
            request.data["user"] = request.user.id

        post = Post.objects.filter(pk=pk).first()
        if post is not None:
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {"msg": "Post Updated Partially!"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"errors": {"msg": "Invalid Post Id!"}},
            status=status.HTTP_400_BAD_REQUEST,
        )


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        post = Post.objects.filter(pk=pk).first()
        if int(request.user.id) != int(post.user.id):
            return Response(
                {
                    "errors": {
                        "msg":
                        "You do not have permission to perform this action."
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if post is not None:
            post.delete()
            return Response(
                {"msg": "Post Deleted Successfully!"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"errors": {"msg": "Invalid Post Id!"}},
            status=status.HTTP_400_BAD_REQUEST,
        )


class PostCommentsListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        likes = comments = 0
        post_data = {}

        all_comments = Comment.objects.filter(post=pk)
        if all_comments is not None:
            comment_serializer = CommentSerializer(all_comments, many=True)
            comments = len(comment_serializer.data)
            post_data["Count Of Comments"] = comments
            post_data["Comments"] = comment_serializer.data

        all_likes = Like.objects.filter(post=pk)
        if all_likes is not None:
            like_serializer = LikeSerializer(all_likes, many=True)
            likes = len(like_serializer.data)
            post_data["Count Of Likes"] = likes

        if likes == 0 and comments == 0:
            return Response(
                {"msg": "No Likes and Comments on this Post!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(post_data, status=status.HTTP_200_OK)


class LikeCreateAPIView(CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOwner]

    def post(self, request, *args, **kwargs):
        if "user" not in request.data:
            request.data["user"] = request.user.id

        user_id = int(request.data["user"])
        post_id = request.data["post"]
        likes = Like.objects.filter(user=user_id, post=post_id).exists()

        if likes:
            return Response(
                {"msg": "Already Liked!"}, status=status.HTTP_200_OK
            )

        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"msg": "Liked Successfully!"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeRetrieveAPIView(RetrieveAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        like = Like.objects.filter(pk=pk).first()
        if like is not None:
            serilizer = LikeSerializer(like)
            return Response(serilizer.data, status=status.HTTP_200_OK)
        return Response(
            {"errors": {"msg": "Invalid Like Id!"}},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LikeListAPIView(ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    # permission_classes = [IsAuthenticated]


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        comments = Comment.objects.filter(user=pk)
        if comments:
            serializer = CommentSerializer(comments, many=True)
            return Response(
                {
                    "Count Of Comments": len(serializer.data),
                    "Comments": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"msg": "No Comments available for this User!"},
            status=status.HTTP_404_NOT_FOUND,
        )


class FollowersListAPIView(ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowersSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        followers = Follow.objects.filter(user_following=pk)
        if followers:
            serializer = FollowersSerializer(followers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"msg": "No Followers for this User!"},
            status=status.HTTP_404_NOT_FOUND,
        )


class FollowingListAPIView(ListAPIView):
    queryset = Follow.objects.all()
    # serializer_class = FollowingsSerializer
    serializer_class = FollowingsSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        following = Follow.objects.filter(user=pk)
        if following:
            serializer = FollowingsSerializer(following, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"msg": "No Followings for this User!"},
            status=status.HTTP_404_NOT_FOUND,
        )
