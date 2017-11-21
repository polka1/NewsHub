from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from rango.models import Category, Page, Post, PortalPost
from rango.forms import CategoryForm, PageForm, UserProfile, UserProfileForm, UserForm
import json
import xmltodict
import requests


# Create your views here.


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {
        'boldmessage': 'Адмiнка',
        'categories': category_list,
        'pages': pages_list
    }
    return render(request, 'rango/index.html', context=context_dict)
    # return HttpResponse("Tango with Django on the rango! <br/>\
    # <a href='/rango/about/'>About</a>.")


def nenoy(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {
        'boldmessage': 'Адмiнка',
        'categories': category_list,
        'pages': pages_list
    }
    return render(request, 'rango/nenoy.html', context=context_dict)
    # return HttpResponse("Tango with Django on the rango! <br/>\
    # <a href='/rango/about/'>About</a>.")


def about(request):
    print(request.method)
    print(request.user)
    context_dict = {
        'linkedin': 'https://linkedin.com/in/grizzzzzzzly/',
        'github': 'https://github.com/polka1',
    }
    return render(request, 'rango/about.html', context_dict)


def main_page(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {
        'boldmessage': 'Адмiнка',
        'categories': category_list,
        'pages': pages_list,
        'test': 'kurvamat'
    }
    return render(request, 'rango/main-page.html', context_dict)


def hindex(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {
        'boldmessage': 'Адмiнка',
        'categories': category_list,
        'pages': pages_list,
        'test': 'kurvamat',
    }
    my_view(request)
    try:
        print("Posts count: ", Post.objects.count())
        post_list = Post.objects.order_by('-updated_at')[:Post.objects.count()]
        context_dict['posts'] = post_list
    except Exception as ex:
        post_list = "No posts"
        print(ex)
        context_dict['posts'] = post_list

    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    context_dict['posts'] = contacts

    return render(request, 'rango/hindex.html', context_dict)


def my_view(request):

    # Let's assume that the visitor uses an iPhone...
    request.user_agent.is_mobile # returns True
    request.user_agent.is_tablet # returns False
    request.user_agent.is_touch_capable # returns True
    request.user_agent.is_pc # returns False
    request.user_agent.is_bot # returns False

    # Accessing user agent's browser attributes
    request.user_agent.browser  # returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')
    request.user_agent.browser.family  # returns 'Mobile Safari'
    request.user_agent.browser.version  # returns (5, 1)
    request.user_agent.browser.version_string   # returns '5.1'

    # Operating System properties
    request.user_agent.os  # returns OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')
    request.user_agent.os.family  # returns 'iOS'
    request.user_agent.os.version  # returns (5, 1)
    request.user_agent.os.version_string  # returns '5.1'

    # Device properties
    request.user_agent.device  # returns Device(family='iPhone')
    request.user_agent.device.family  # returns 'iPhone'
    print('###')
    print(request.user_agent.device)
    print(request.user_agent.os)
    print(request.user_agent.browser)
    print(request.environ['REMOTE_ADDR'])
    # print(request.environ['HTTP_X_FORWARDED_FOR'])
    # print(request.environ.get('HTTP_X_REAL_IP', request.environ['REMOTE_ADDR']))
    print('###\n')


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Имеем ли действительную форму?
        if form.is_valid():
            # Сохраняем новую форму в БД
            form.save(commit=True)
            return index(request)
        else:
            # В форме ошибка
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.save()

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def news24():
    url = 'http://24tv.ua/rss/all.xml'
    req = requests.get(url)
    # print(req.text)

    parsed = xmltodict.parse(req.text)
    # print(parsed)
    parsed_json = json.dumps(parsed, ensure_ascii=False)
    # print(parsed['rss'])
    title = parsed['rss']['channel']['item'][0]['title']
    title_list = str(title).split(" ")
    title_list = [substr for substr in title_list if len(substr) < 30]
    title = " ".join(title_list)
    link = parsed['rss']['channel']['item'][0]['link']
    description = parsed['rss']['channel']['item'][0]['description'][:1024]
    post_date = parsed['rss']['channel']['item'][0]['pubDate']
    post = Post()
    try:
        p_obj = Post.objects.last()
    except:
        p_obj = None
    print('--------------')
    print(p_obj.post_date)
    print(post_date)
    if str(p_obj.post_date) != str(post_date) and p_obj.title != title:
        post.title = title
        post.description = description
        post.url = link
        post.post_date = post_date
        post.save()

        print(title)
        print(link)
        print(description)
        print(post_date)


def news24_upload_all():
    url = 'http://24tv.ua/rss/all.xml'
    req = requests.get(url)
    # print(req.text)
    parsed = xmltodict.parse(req.text)
    count = len(parsed['rss']['channel']['item'])
    for i in range(0, count):

        title = parsed['rss']['channel']['item'][i]['title']
        title_list = str(title).split(" ")
        title_list = [substr for substr in title_list if len(substr) < 30]
        title = " ".join(title_list)
        link = parsed['rss']['channel']['item'][i]['link']
        description = parsed['rss']['channel']['item'][i]['description'][:1024]
        post_date = parsed['rss']['channel']['item'][i]['pubDate']
        post = Post()
        try:
            p_date = Post.objects.all()[Post.objects.count()-1].post_date
        except:
            p_date = None
        print('--------------')
        print(p_date)
        print(post_date)
        if str(p_date) != str(post_date):
            post.title = title
            post.description = description
            post.url = link
            post.post_date = post_date
            post.save()

            print(title)
            print(link)


def news112():
    url = "https://ua.112.ua/rss/index.rss"
    req = requests.get(url)
    parsed = xmltodict.parse(req.text)
    title = parsed['rss']['channel']['item'][0]['title']
    link = parsed['rss']['channel']['item'][0]['link']
    description = parsed['rss']['channel']['item'][0]['description'][:1024]
    date = parsed['rss']['channel']['item'][0]['pubDate']
    post = Post()
    try:
        p_date = Post.objects.all()[Post.objects.count() - 1].date
    except:
        p_date = None
    print('--------------')
    print(p_date)
    print(date)
    if str(p_date) != str(date):
        post.title = title
        post.description = description
        post.url = link
        post.date = date
        post.save()

        print(title)
        print(link)


def portal_posts(request):
    context_dict = {
        'boldmessage': 'Адмiнка',
        'test': 'kurvamat',
    }
    my_view(request)
    try:
        post_list = PortalPost.objects.order_by('-updated_at')[:PortalPost.objects.count()]
        context_dict['posts'] = post_list
    except Exception as ex:
        post_list = "No posts"
        print(ex)
        context_dict['posts'] = post_list

    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context_dict['posts'] = posts

    return render(request, 'rango/portal_news.html', context_dict)

def hindex_tverezo(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {
        'boldmessage': 'Адмiнка',
        'categories': category_list,
        'pages': pages_list,
        'test': 'kurvamat',
    }
    my_view(request)
    try:
        print("Posts count: ", Post.objects.count())
        post_list = Post.objects.filter(provider='tverezo').order_by('-updated_at')[:Post.objects.count()]
        context_dict['posts'] = post_list
    except Exception as ex:
        post_list = "No posts"
        print(ex)
        context_dict['posts'] = post_list

    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    context_dict['posts'] = contacts

    return render(request, 'rango/hindex.html', context_dict)


def hindex_news24(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {
        'boldmessage': 'Адмiнка',
        'categories': category_list,
        'pages': pages_list,
        'test': 'kurvamat',
    }
    my_view(request)
    try:
        print("Posts count: ", Post.objects.count())
        post_list = Post.objects.filter(provider='news24').order_by('-updated_at')[:Post.objects.count()]
        context_dict['posts'] = post_list
    except Exception as ex:
        post_list = "No posts"
        print(ex)
        context_dict['posts'] = post_list

    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    context_dict['posts'] = contacts

    return render(request, 'rango/hindex.html', context_dict)


def hindex_informn(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {
        'boldmessage': 'Адмiнка',
        'categories': category_list,
        'pages': pages_list,
        'test': 'kurvamat',
    }
    my_view(request)
    try:
        print("Posts count: ", Post.objects.count())
        post_list = Post.objects.filter(provider='inform_napalm').order_by('-updated_at')[:Post.objects.count()]
        context_dict['posts'] = post_list
    except Exception as ex:
        post_list = "No posts"
        print(ex)
        context_dict['posts'] = post_list

    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    context_dict['posts'] = contacts

    return render(request, 'rango/hindex.html', context_dict)
