from django.contrib import admin
from rango.models import Category, Page, PortalPost, Post
from rango.models import UserProfile
# Register your models here.


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


class PortalNews(admin.ModelAdmin):
    news = {'title', 'post_date'}


class Posts(admin.ModelAdmin):
    news = {'title', 'provider', 'post_date'}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
admin.site.register(PortalPost, PortalNews)
admin.site.register(Post, Posts)
