from django.contrib import admin
from .models import Category, Post


def nullfy_articles(modeladmin, request, queryset):
    queryset.update(quantity=0)


nullfy_articles.short_description = 'Удолить статьи'


class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'on_stock')
    list_filter = ('author', 'category', 'raiting')
    search_fields = ('name', 'author__name')
    actions = [nullfy_articles]


admin.site.register(Category)
admin.site.register(Post, PostAdmin)

