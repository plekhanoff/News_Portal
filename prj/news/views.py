from datetime import datetime
from .models import models
from .tasks import read_post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, DeleteView, UpdateView, DetailView,
)
from django.core.cache import cache
from .filters import *
from .forms import *
from django.views.decorators.cache import cache_page
import logging
from django.utils.translation import gettext as _  # импортируем функцию для перевода


# Create your views here.
logger = logging.getlogger(__name__)


@cache_page(
    60 * 8)
def my_view(request):
    ...

def index(request):
    news = News.objects.all()

    return render(request, "index.html",context={'news': news})


def detail(request,slug):
    new = News.objects.get(slug__iexact = slug)
    return render(request, "detail.html", context={'new': new})


class PostList(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'index'
    paginate_by = 2

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.filterset = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'detail.html'
    context_object_name = 'detail'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'index-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'index-{self.kwargs["pk"]}', obj)
            return obj


class NewsCreate(CreateView):
    form_class = PostForm
    model = News
    template_name = 'post_edit.html'
    context_object_name = 'post_edit'

class NewsEdit(UpdateView):
    form_class = PostForm
    model = News
    template_name = 'post_edit.html'
    context_object_name = 'post_edit'

    def form_valid(self, form):
        news = form.save(commit=False)
        return super().form_valid(form)


class NewsDelete(DeleteView):
    model = News
    form_class = PostForm
    template_name = 'post_delete.html'
    context_object_name = 'post_delete'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        news = form.save(commit=False)
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Article
    template_name = 'post_edit.html'
    context_object_name = 'post_edit'


class ArticleEdit(UpdateView):
    form_class = PostForm
    model = Article
    template_name = 'post_edit.html'
    context_object_name = 'post_edit'

    def form_valid(self, form):
        article = form.save(commit=False)
        return super().form_valid(form)


class ArticleDelete(DeleteView):
    form_class = PostForm
    model = Article
    template_name = 'post_delete.html'
    context_object_name = 'post_delete'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        article = form.save(commit=False)
        return super().form_valid(form)


class Search(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'


class PostCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class CategoryListView(ListView):
    model = Post
    template_name = 'news/category_lst.html'
    context_object_name = 'category_news_list'

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.user = None
        self.request = None
        self.kwargs = None


    def get_queryset(self):
        self.category = get_object_or_404(Category,id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request,pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'вы успешно подписаны на категорию'
    return render(request, 'news/subscribe.html',{'category': category, 'message': message})


class NewPostView(CreateView):
    model = Post
    fields = ['title']
    template_name = 'news/new_post.html'

    def form_valid(self, form):
        post = form.save()
        post.save()
        read_post.apply_async([post.pk])
        return redirect('/')


def read_post(request, id):
    post = Post.objects.get(pk=id)
    post.time_out = datetime.now()
    post.save()
    return redirect('/')


