
from celery import shared_task

from .models import Post


@shared_task
def read_post(id):
    post = Post.objects.get(pk = id)
    post.read = True
    post.save()
