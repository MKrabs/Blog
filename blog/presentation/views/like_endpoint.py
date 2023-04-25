from django.shortcuts import redirect

from blog.application.like_service import LikeService


class LikeEndpoint:

    like_service = LikeService()

    @classmethod
    def liked(cls, request, post_id):
        if request.user.is_authenticated:
            cls.like_service.toggle_like(post_id=post_id, author_id=request.user)

        return redirect('post', post_id)
