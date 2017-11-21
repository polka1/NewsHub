from django.conf.urls import url
from rango import views
from django.views.generic import RedirectView


app_name = 'rango'
urlpatterns = [ 
    url(r'^$', views.hindex, name='index'),
    url(r'^nenoy$', views.nenoy, name='nenoy'),
    url(r'^hindex$', views.hindex, name='hindex'),
    url(r'^filter-news24$', views.hindex_news24, name='filter-news24'),
    url(r'^filter-tverezo$', views.hindex_tverezo, name='filter-tverezo'),
    url(r'^filter-informn$', views.hindex_informn, name='filter-informn'),
    url(r'^about/$', views.about, name='about'),
    url(r'^portal-news$', views.portal_posts, name='portal-news'),
    # url(r'^main-page$', views.main_page, name='main-page'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico?v=2')),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
]
