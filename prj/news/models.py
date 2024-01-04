from allauth.conftest import user
from django.shortcuts import reverse
from django.db import models
from django.db.models import Sum
from django.core.cache import cache
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User


class Author(models.Model):
    AuthorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)
    dateCreation = models.DateTimeField(auto_now_add=True)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum("rating")) or {"postRating": 0}
        pRat = postRat["postRating"]

        commentRat = self.AuthorUser.comment_set.aggregate(commentRating=Sum("rating")) or {"commentRating": 0}
        cRat = commentRat["commentRating"]

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=64,unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.name


class Post(models.Model):
    objects = None
    author = models.ForeignKey(Author,on_delete = models.CASCADE)
    NEWS = "NW"
    ARTICLE = "AR"
    CATEGORY_CHOICES = ((NEWS,"Новость"),(ARTICLE,"Статья"))
    category_type = models.CharField(max_length = 2,choices = CATEGORY_CHOICES,default = ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through = "PostCategory")
    title = models.CharField(max_length = 128)
    text = models.TextField()
    rating = models.SmallIntegerField(default = 0)

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()

    def preview(self):
        return self.text[0:123] + "..."

    def __str__(self):
        return f'{self.author.name()}: {self.category_type}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def get_context_data(self, param):
        pass

    def __str__(self):
        return f'{self.title} {self.text}'

    def get_absolute_url(self):
        return f'/index/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'index-{self.pk}')


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post,on_delete = models.CASCADE)
    CategoryThrough = models.ForeignKey(Category,on_delete = models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post,on_delete = models.CASCADE)
    commentUser = models.ForeignKey(User,on_delete = models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add = True)
    rating = models.SmallIntegerField(default = 0)

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()

    def preview(self):
        return self.text[0:123] + "..."


class News(models.Model):
    objects = ()
    title = models.CharField(max_length=64)
    text = models.TextField()
    date_pub = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=128, unique=True)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['-date_pub']


class Article (models.Model):
    objects = ()
    title = models.CharField(max_length=64)
    text = models.TextField()
    date_pub = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=128, unique=True)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['-date_pub']

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Email должен быть установлен')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email', max_length=60, unique=True)
    username = models.CharField(verbose_name='Имя пользователя', max_length=30, unique=True)
    # Добавьте дополнительные поля, если требуется

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
