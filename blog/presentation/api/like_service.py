from django.shortcuts import redirect

from blog.domain.entities.like import Like
from blog.domain.entities.post import Post


class LikeService:

    @classmethod
    def liked(cls, request, post_id):
        if request.user.is_authenticated:
            post = Post.objects.get(id=post_id)
            like = Like.objects.filter(author=request.user, post_id=post)
            if like.count() < 1:
                Like(author=request.user, post=post).save()
            else:
                like.delete()

        return redirect('post', post_id)
