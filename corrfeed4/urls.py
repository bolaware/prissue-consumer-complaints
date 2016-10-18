"""corrfeed4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include,patterns
from django.contrib import admin
from corrfeed import views
from django.conf import settings

from corrfeed.views import AuthorityAutocomplete
from django.conf.urls.static import static

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^prof-change/gdyu734648dgey83y37gyyeyu8g/',views.login_redir,name='login_redir'),
    url(r'^$',views.home,name='home'),
    url(r'^about/$',views.about,name='about'),
    url(r'^random-ten/$',views.random_ten,name='random_ten'),
    url(r'^report/(?P<pk>\d+)/$',views.report,name='report'),
    url(r'^save/(?P<pk>\d+)/$',views.save,name='archive'),
    url(r'^post-feed/$',views.post_feed,name='post_feed'),
    url(r'^(?P<username>\w+)/following/$',views.following,name='following'),
    url(r'^archive/$',views.archive,name='archive_detail'),
    url(r'^categories/$',views.category,name='category'),
    url(r'^authority/highest-corruption-feed/$',views.authority_highest_feed,name='authority_highest_feed'),
    url(r'^highest-corruption-feed-concerns/$',views.highest_concerned_feeds,name='highest_concerned_feeds'),
    url(r'^organization/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',views.authority_details,name='authority_details'),
    url(r'^feed/(?P<slug>[-\w]+)/$',views.feed_detail,name='feed_detail'),
    url(r'^like/$', views.like, name='like'),
    url(r'^experience/$', views.experience, name='experience'),
    url(r'^authority-autocomplete/$',AuthorityAutocomplete.as_view(),name='authority-autocomplete',),
    url(r'^create-profile/(?P<username>\w+)/$',views.add_profile,name='create-profile'),
    url(r'^create-authority/$',views.submit_authority,name='create-authority'),
    url(r'^edit-feed/(?P<pk>\d+)/$',views.edit_feed,name='edit_feed'),
    url(r'^results/$',views.search,name='search'),
    url(r'^user/(?P<username>\w+)/$',views.user_profile,name='user_profile'),
    url(r'^stats/(?P<pk>\d+)/$',views.chart,name='stats'),
    url(r'^follow-category/$',views.follow_cat,name='follow_cat'),
    url(r'^follow-organization/$',views.follow_org,name='follow_org'),
    url(r'^category/(?P<slug>[-\w]+)/$',views.category_detail,name='category_detail'),
    url(r'^category/organizations/(?P<slug>[-\w]+)/$',views.category_auth,name='category_auth'),
    url(r'^progressbarupload/', include('progressbarupload.urls')),
]
urlpatterns += patterns('',(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),)





