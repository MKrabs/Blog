from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from blog.domain.entities.comment import Comment
from blog.domain.entities.post import Post


class CommentService:
    @classmethod
    def comment(cls, request, post_id):
        if request.method == 'POST' and len(request.POST['commentBody']) > 0:
            comm = Comment()
            comm.author = request.user if request.user.is_authenticated and not request.POST.get('anonymous') else None
            comm.post = Post.objects.get(id=post_id)
            comm.body = request.POST['commentBody']
            comm.save()
            messages.success(request, f'Comment "{comm.body[:10]}..." was posted.')
        else:
            messages.warning(request, 'Warning: Message can not be empty.')

        return redirect(reverse('post', kwargs={'post_id': post_id}) + '#comments')

    @classmethod
    def comment_delete(cls, request, post_id, comm_id):
        if request.method == 'POST' and request.user.is_authenticated:
            comm = Comment.objects.get(id=comm_id)
            if request.user == comm.author:
                comm.delete()
                messages.info(request, f'Comment "{comm.body[:10]}..." was deleted.')
        else:
            messages.error(request, f'Comment n°{comm_id} could not be deleted.')

        return redirect(reverse('post', kwargs={'post_id': post_id}) + '#comments')