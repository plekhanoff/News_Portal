
from django.urls import path
from django.views.decorators.cache import cache_page
from prj.news.views import *

urlpatterns = [
    path('news_list/',index, name = 'index'),
    path('news/<str:slug>',detail,cache_page(60*1), name = 'detail'),
    path('news/create/', NewsCreate.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='post_edit'),
    path('article/create/', ArticleCreate.as_view(), name='post_edit'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='post_delete'),
    path('article/<int:pk>/edit/', ArticleEdit.as_view(), name='post_edit'),
    path('search/',Search.as_view(), name='search'),
    path('categories/<int:pk>',cache_page(60*1),CategoryListView.as_view(),name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('new/', NewPostView.as_view(), name='new_post'),
]


