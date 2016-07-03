#-*-coding:utf-8-*-
from django.shortcuts import render,redirect
from corrfeed.models import Feed,Authority
from django.utils import timezone
from django.db.models import Count
from django.shortcuts import render,get_object_or_404
from forms import FeedForm
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


def home(request):
    concern='Concern'
    feeds=Feed.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    return render(request , 'index.html' ,{'feeds':feeds,'form':FeedForm(),'feed_detail':feed_detail,})
    
def authority_highest_feed(request):
    auth_with_highest_feeds=Authority.objects.annotate(num_feeds=Count('feed')).order_by('-num_feeds')
    return render(request , 'highest_authority.html' ,{'auth_with_highest_feeds':auth_with_highest_feeds})

def highest_concerned_feeds(request):
    feed_highest_concerns=Feed.objects.annotate(Count('user_concerns')).order_by('-user_concerns__count')
    return render(request , 'concerned_feeds.html' ,{'feed_highest_concerns':feed_highest_concerns})
    
def authority_details(request,pk):
    authority=get_object_or_404(Authority,pk=pk)
    authority_feeds=authority.feed_set.all().order_by('-pub_date')
    no_of_feed_per_authority=authority.feed_set.all().count()
    no_of_resolved_feed_per_authority=authority.feed_set.filter(resolved=True).count()
    return render(request, 'authority_detail.html' ,{'authority':authority,'authority_feeds':authority_feeds,'no_of_feed_per_authority':no_of_feed_per_authority,
    'no_of_resolved_feed_per_authority':no_of_resolved_feed_per_authority})
    
def post_feed(request):
    form_class = FeedForm
    if request.method == 'POST':
        form = form_class(request.POST,request.FILES)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.user = User.objects.get(pk=1)
            feed.pub_date=timezone.now()
            #instance = Feed(files=request.FILES['files'])
           # feed.files=request.FILES['files']
            feed.save()
            return redirect('home')
    else:
        form = form_class()
        return render(request, 'post_feed.html', {'form': form,})


def feed_detail(request,slug):
    feed_detail=get_object_or_404(Feed,slug=slug)
    return render(request,'feed_detail.html' , {'feed_detail':feed_detail})
   
from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from corrfeed.models import Feed


#@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        feed = get_object_or_404(Feed, slug=slug)

        if feed.user_concerns.filter(id=user.id).exists():
            # user has already liked this company
            # remove like/user
            feed.user_concerns.remove(user)
            message = 'You disliked this'
        else:
            # add a new like for a company
            feed.user_concerns.add(user)
            message = 'You liked this'

    ctx = {'likes_count': feed.total_concerns, 'message': message}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')  
        
    
    
    
    

    
    
   