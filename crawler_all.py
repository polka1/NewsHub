#import postgresql
import time

import re
import requests
import xmltodict
import json
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango.settings')
import django
django.setup()
from rango.models import Post


with open('/home/debian/IT/virtualenvs/reborn_django/tango/crawler_all.pid', 'w') as f:
    pid = str(os.getpid())
    f.write("%s" % pid)
    print("PID: ", pid)


def news24():
    url = 'http://24tv.ua/rss/all.xml'
    provider = 'news24'
    req = requests.get(url)
    parsed = xmltodict.parse(req.text)
    parsed_json = json.dumps(parsed, ensure_ascii=False)
    title = parsed['rss']['channel']['item'][0]['title']
    title_list = str(title).split(" ")
    title_list = [substr for substr in title_list if len(substr) < 30]
    title = " ".join(title_list)
    link = parsed['rss']['channel']['item'][0]['link']
    description = parsed['rss']['channel']['item'][0]['description'][:1024]
    post_date = parsed['rss']['channel']['item'][0]['pubDate']
    img_src = re.findall(r"src='(.*?)'", description)[0]
    description_without_img = str(description).replace(re.match(r"(.*?).jpg'>",
                                                                description).group(0), "")
    post = Post()
    try:
        p_obj = Post.objects.filter(provider='news24')[Post.objects.filter(provider='news24').count() - 1]
        print('####################')
        print('-------news24-------')
        print(p_obj.post_date)
        print(post_date)
        if p_obj.img != img_src and p_obj.provider == provider:
            # str(p_obj.post_date) != str(post_date) and p_obj.title != title
            post.title = title
            post.url = link
            post.post_date = post_date
            post.img = img_src
            post.description = description_without_img
            post.provider = provider

            post.save()
            print('POST INFO: ')
            print(title)
            print(post_date)

    except Exception as err:
        print(err)


def tverezo():
    url = 'http://tverezo.info/feed'
    provider = 'tverezo'
    req = requests.get(url)
    parsed = xmltodict.parse(req.text)
    title = parsed['rss']['channel']['item'][0]['title']
    title_list = str(title).split(" ")
    title_list = [substr for substr in title_list if len(substr) < 30]
    title = " ".join(title_list)
    link = parsed['rss']['channel']['item'][0]['link']
    description = parsed['rss']['channel']['item'][0]['description'][:1024]
    post_date = parsed['rss']['channel']['item'][0]['pubDate']
    img_src = re.findall(r"src='(.*?)'", description)
    if img_src:
        description_without_img = str(description).replace(re.match(r"(.*?).jpg'>",
                                                                    description).group(0), "")
    else:
        # img_src = "No link"
        description_without_img = description
    post = Post()
    try:
        p_obj = Post.objects.filter(provider='tverezo')[Post.objects.filter(provider='tverezo').count() - 1]
        img_src = p_obj.img
        print('-------tverezo------')
        print(p_obj.post_date)
        print(post_date)
        if str(p_obj.post_date) != str(post_date) and p_obj.title != title and p_obj.provider == provider:
            post.title = title
            post.url = link
            post.post_date = post_date
            post.img = img_src
            post.description = description_without_img
            post.provider = provider

            post.save()
            print('POST INFO:')
            print(title)
            print(post_date)
    except Exception as err:
        print(err)


def inform_napalm():
    url = 'https://informnapalm.org/feed/'
    provider = 'inform_napalm'
    req = requests.get(url)

    parsed = xmltodict.parse(req.text)
    title = parsed['rss']['channel']['item'][0]['title']
    title_list = str(title).split(" ")
    title_list = [substr for substr in title_list if len(substr) < 30]
    title = " ".join(title_list)
    link = parsed['rss']['channel']['item'][0]['link']
    description = parsed['rss']['channel']['item'][0]['description'][:1024]
    post_date = parsed['rss']['channel']['item'][0]['pubDate']
    img_src = re.findall(r"src='(.*?)'", description)
    if img_src:
        img_src = img_src[0]
        description_without_img = str(description).replace(re.match(r"(.*?).jpg'>",
                                                                    description).group(0), "")
    else:
        description_without_img = description
    post = Post()
    try:
        p_obj = Post.objects.filter(provider='inform_napalm')[Post.objects.filter(provider='inform_napalm').count() - 1]
        img_src = p_obj.img
        print('-------inform_napalm---')
        print(p_obj.post_date)
        print(post_date)
        if str(p_obj.post_date) != str(post_date) and p_obj.title != title and p_obj.provider == provider:
            post.title = title
            post.url = link
            post.post_date = post_date
            post.img = img_src
            post.description = description_without_img
            post.provider = provider

            post.save()
            print('POST INFO:')
            print(title)
            print(post_date)
        print('####################\n')
    except Exception as err:
        print(err)


def main():
    while True:
        try:
            news24()
        except Exception as er:
            print(er)
        try:
            tverezo()
        except Exception as er:
            print(er)
        try:
            inform_napalm()
        except Exception as er:
            print(er)
        time.sleep(100)


main()
