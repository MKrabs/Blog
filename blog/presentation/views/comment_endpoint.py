from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from blog.application.comment_service import CommentService
from blog.application.post_service import PostService


class CommentEndpoint:
    comment_service = CommentService()
    post_service = PostService()

    @classmethod
    def comment(cls, request, post_id):
        if request.method == 'POST' and len(request.POST['commentBody']) > 0:
            post = cls.post_service.get_post_by_id(post_id=post_id)
            author = request.user if request.user.is_authenticated and not request.POST.get('anonymous') else None
            body = request.POST['commentBody']

            cls.comment_service.create_comment(
                author=author,
                post_id=post.id,
                body=body,
            )

            messages.success(request, f'Comment "{body[:10]}..." was posted.')
        else:
            messages.warning(request, 'Warning: Message can not be empty.')

        return redirect(reverse('post', kwargs={'post_id': post_id}) + '#comments')

    @classmethod
    def comment_delete(cls, request, post_id, comment_id):
        if not (request.method == 'POST' and request.user.is_authenticated):
            messages.error(request, f'Comment n°{comment_id} could not be deleted.')

        comment = cls.comment_service.get_comment_by_id(comment_id=comment_id)

        if request.user == comment.author:
            cls.comment_service.delete_comment(comment_id=comment_id)
            messages.info(request, f'Comment "{comment.body[:10]}..." was deleted.')

        return redirect(reverse('post', kwargs={'post_id': post_id}) + '#comments')
