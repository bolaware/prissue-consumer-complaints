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
    url(r'^post-feed/$',views.post_feed,name='post_feed'),
    url(r'^post-comment/(?P<pk>\d+)/$',views.post_comment,name='post_comment'),
    url(r'^authority/highest-corruption-feed/$',views.authority_highest_feed,name='authority_highest_feed'),
    url(r'^highest-corruption-feed-concerns/$',views.highest_concerned_feeds,name='highest_concerned_feeds'),
    url(r'^authority/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',views.authority_details,name='authority_details'),
    url(r'^feed/(?P<slug>[-\w]+)/$',views.feed_detail,name='feed_detail'),
    url(r'^like/$', views.like, name='like'),
    url(r'^auth-card/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',views.auth_card,name='auth_card'),
    url(r'^experience/$', views.experience, name='experience'),
    url(r'^authority-autocomplete/$',AuthorityAutocomplete.as_view(),name='authority-autocomplete',),
    url(r'^create-profile/(?P<username>\w+)/$',views.add_profile,name='create-profile'),
    url(r'^create-authority/$',views.submit_authority,name='create-authority'),
    url(r'^edit-feed/(?P<pk>\d+)/$',views.edit_feed,name='edit_feed'),
    url(r'^results/$',views.search,name='search'),
    url(r'^user/(?P<username>\w+)/$',views.user_profile,name='user_profile'),
    url(r'^stats/(?P<pk>\d+)/$',views.chart,name='stats'),
   # url(r'^profile/(?P<slug>[-\w]+)/$',views.profile_details,name='profile_details')
]
urlpatterns += patterns('',(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),)





