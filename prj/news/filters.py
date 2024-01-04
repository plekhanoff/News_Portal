from .models import *
import django_filters


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['category', 'title', 'dateCreation']