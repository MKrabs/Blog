from django.shortcuts import render

from blog.application.post_service import PostService


class HomepageView:
    post_service = PostService()

    @classmethod
    def index(cls, request, page=1):
        latest_posts = cls.post_service.get_latest_posts(user=request.user, order_by='-date', additional_fields=True)
        p, num_pages = cls.post_service.paginate_posts(latest_posts, param=4, page=page)

        context = {
            'page': {
                'current': p.number,
                'total': num_pages,
            },
            'latest_posts': p.object_list,
        }

        return render(request, 'blog/index.html', context)

    @classmethod
    def page_not_found(cls, request, pattern):
        context = {
            'broken': pattern
        }

        return render(request, 'blog/404.html', context)
