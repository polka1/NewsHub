from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    likes = models.IntegerField(verbose_name='Like', default=0)
    views = models.IntegerField(verbose_name='Views', default=0)
    slug = models.SlugField(null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile)images', blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=128)
    url = models.URLField()
    description = models.CharField(max_length=1024)
    post_date = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    img = models.URLField(blank=True)
    provider = models.CharField(max_length=24)

    class Meta:
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.title


class PortalPost(models.Model):
    title = models.CharField(max_length=128)
    url = models.URLField()
    description = models.CharField(max_length=1024)
    post_date = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    img = models.URLField(blank=True)
    provider = models.CharField(max_length=24)

    class Meta:
        verbose_name_plural = 'Portal News'

    def __str__(self):
        return self.title

