#-*-coding:utf-8-*-
from django.shortcuts import render,redirect
from corrfeed.models import Feed,Authority,Category
from django.utils import timezone
from django.db.models import Count
from django.shortcuts import render,get_object_or_404,render_to_response
from forms import FeedForm,CommentsForm
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from  django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def home(request):
    concern='Concern'
    feeds=Feed.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    
        
    paginator = Paginator(feeds,5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        feedz = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        feedz = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        feedz = paginator.page(paginator.num_pages)
    return render_to_response('index.html', {"feeds":feeds,"feedz": feedz,'form':FeedForm(),'feed_detail':feed_detail,},context_instance=RequestContext(request))
    
   # return render(request , 'index.html' ,{'feeds':feeds,'form':FeedForm(),'feed_detail':feed_detail,})
    
def authority_highest_feed(request):
    auth_with_highest_feeds=Authority.objects.annotate(num_feeds=Count('feed')).order_by('-num_feeds')
    paginator = Paginator(auth_with_highest_feeds,10) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        auth= paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        auth = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        auth = paginator.page(paginator.num_pages)
    
    return render(request , 'highest_authority.html' ,{'auth':auth,'auth_with_highest_feeds':auth_with_highest_feeds})

def highest_concerned_feeds(request):
    feeds=Feed.objects.annotate(Count('user_concerns')).order_by('-user_concerns__count')
    paginator = Paginator(feeds,5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        feedz = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        feedz = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        feedz = paginator.page(paginator.num_pages)
    return render(request , 'concerned_feeds.html' ,{'feedz':feedz})
    
def auth_card(request,pk,slug):
    authority=get_object_or_404(Authority,pk=pk)
    no_of_feed_per_authority=authority.feed_set.all().count()
    no_of_resolved_feed_per_authority=authority.feed_set.filter(resolved=True).count()
    percent_resolved=(float(no_of_resolved_feed_per_authority) / no_of_feed_per_authority)*100
    print 'Number of feed= %d'%(no_of_feed_per_authority)
    print 'Resolved=%d'%(no_of_resolved_feed_per_authority)
    print 'percent_resoleved=%d'%(percent_resolved)
    return render(request, 'auth_card.html' , {'authority':authority,'no_of_feed_per_authority':no_of_feed_per_authority,'percent_resolved':percent_resolved})
    
def authority_details(request,pk,slug):
    authority=get_object_or_404(Authority,pk=pk)
    feeds=authority.feed_set.all().order_by('-pub_date')
    no_of_feed_per_authority=authority.feed_set.all().count()
    no_of_resolved_feed_per_authority=authority.feed_set.filter(resolved=True).count()
    #authority.pub_date=timezone.now()
    authority.save()
    paginator = Paginator(feeds,5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        feedz = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        feedz = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        feedz = paginator.page(paginator.num_pages)
        
    ds = DataPool(
       series=
        [{'options': {
            'source': Authority.objects.filter(country=authority.country,category=authority.category).order_by('-pub_date')[:8]},
          'terms': [
            'name',
            'unresolved', 
            'resolved']}
         ])

    cht = Chart(
        datasource = ds, 
        series_options = 
          [{'options':{
              'type': 'column',
              'stacking': False},
            'terms':{
              'name': [
                'unresolved',
                'resolved']
              }}],
        chart_options = 
          {'title': {
               'text': 'Prissue.com Consumer Complaint Data for %s and similiar organizations'%authority.name},
           'xAxis': {
                'title': {
                   'text': '%s and similiar organizations'%authority.name}},
            'yAxis': {
                'title': {
                   'text': "Customer Issues"}}})
    return render(request, 'authority_detail.html' ,{'cht':cht,'authority':authority,'feedz':feedz,'no_of_feed_per_authority':no_of_feed_per_authority,
    'no_of_resolved_feed_per_authority':no_of_resolved_feed_per_authority,})
    

def login_redir(request):
    user=get_object_or_404(User,username=request.user.username)
    username=user.username
    if bool(user.first_name) and bool(user.first_name) ==True:
        return redirect('home')
    return redirect('create-profile',username=username)    
    

from django.contrib.auth.models import User
from .forms import ProfileFormSet, UserForm,AuthorityForm,EditFeedForm
from .models import Profile
from django.http import Http404
    
def add_profile(request,username):
    userman=User.objects.get(username=username)
    if userman != request.user:
        raise Http404
        
    form_class=UserForm
    if request.method=='POST':
         
        form=form_class(data=request.POST,instance=userman)    
        if form.is_valid():
            user = form.save(commit=False)
           
            profile_formset = ProfileFormSet(request.POST, instance=user)
            if profile_formset.is_valid():
                user.save()
                profile_formset.save()
                messages.success(request,'Upadated profile successfully')
                #return HttpResponseRedirect(reverse('user_profile_submitted'))
                return redirect('home')
    else:
        form = form_class(instance=userman)
        profile_formset = ProfileFormSet(instance=userman)
    return render(request,'create_profile.html',{"form": form,"profile_formset": profile_formset,})

    
def submit_authority(request):
    categories=Category.objects.all()
    form_class=AuthorityForm
    if request.method=="POST":
        form=form_class(request.POST)
        if form.is_valid():
            authority=form.save(commit=False)
            authority.save()
            return redirect("authority_details",pk=authority.pk,slug=authority.slug)
            
    else:
        form=form_class()
    return render(request,'create_authority.html',{'categories':categories,'form':form})
    
from .forms import EditAuthorityForm
def edit_authority(request,pk):
    authority=get_object_or_404(Authority,pk=pk)
    form_class=EditAuthorityForm
    if request.method=='POST':
        form=form_class(data=request.POST,instance=authority)
        if form.is_valid():
            form_feed=form.save(commit=False)
            form_feed=form.save()
            return redirect('feed_detail',pk=form_feed.slug,slug=form_feed.slug)
    else:
        form=form_class(instance=authority)
    return render(request,'edit_authority.html',{'form':form,})
    
    

    
def edit_feed(request,pk):
    feed=get_object_or_404(Feed,pk=pk)
    form_class=EditFeedForm
    if request.method=='POST':
        form=form_class(request.POST,request.FILES,instance=feed)
        if form.is_valid():
            form_feed=form.save(commit=False)
            form_feed=form.save()
            return redirect('feed_detail',slug=form_feed.slug)
    else:
        form=form_class(instance=feed)
    return render(request,'edit_feed.html',{'form':form,})
    



'''def search(request):
    form_class=SearchForm
    if request.method=='GET':
        term=request.GET['sum']   
        authority=Authority.objects.filter(name__icontains='term')
        feeds=authority.feed_set.all()
        return render(request,'feed_list.html',{'feeds':feeds})    
    else:
        form=form_class()
    return render(request,'search.html',{'form':form})'''
    
def search(request):
  if 'q' in request.GET:
    if request.GET['q'] == '':
      message = 'No searching keyword entered'
    else:
      something=request.GET['q']
      message = 'You searched for: %s' % request.GET['q']
      authority=Authority.objects.filter(name__icontains=something)
      paginator = Paginator(authority,10) 
      page = request.GET.get('page')
      try:
          auth= paginator.page(page)
      except PageNotAnInteger:
        # If page is not an integer, deliver first page.
          auth = paginator.page(1)
      except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
          auth = paginator.page(paginator.num_pages) 
      
      return render(request,'search_result.html',{'auth':auth})
      #return redirect('home')
  else:
      message = 'Form is not submitted properly.'
  return HttpResponse(message)

        
 
from django.contrib import messages
def post_feed(request):
    user=request.user
    if bool(user.first_name) and bool(user.first_name) ==True:
        concern='Concern'
        feeds=Feed.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
        paginator = Paginator(feeds,5) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            feedz = paginator.page(page)
        except PageNotAnInteger:
            feedz = paginator.page(1)
        except EmptyPage:
            feedz = paginator.page(paginator.num_pages)
        form_class = FeedForm
        if request.method == 'POST':
            form = form_class(request.POST,request.FILES)
            if form.is_valid():
                feed = form.save(commit=False)
                feed.user = user
                feed.pub_date=timezone.now()
                feed.save()
                messages.success(request,'Issue successfully posted.')
                #return render(request , 'index.html' ,{'c':c,'feeds':feeds,"feedz": feedz,'form':FeedForm(),'feed_detail':feed_detail,})
                return redirect('home')
                #return render_to_response('index.html', {"feeds":feeds,"feedz": feedz,'form':FeedForm(),'feed_detail':feed_detail,},context_instance=RequestContext(request))
        else:
            form = form_class()
        return render(request , 'index.html' ,{'feeds':feeds,"feedz": feedz,'form':form,'feed_detail':feed_detail,})
    else:
        messages.success(request,'ERROR,Update your profile before posting!')
    return redirect('create-profile',username=user.username)
    
    
    #return redirect('home')
    #return render_to_response('index.html', {"feeds":feeds,"feedz": feedz,'form':form,'feed_detail':feed_detail,},context_instance=RequestContext(request))
        
        #return render_to_response('index.html', {"feeds": feeds,'form':FeedForm(),'feed_detail':feed_detail,})

import os
def feed_detail(request,slug):
    feed_detail=get_object_or_404(Feed,slug=slug)
    comment_of_feed_count=feed_detail.comments_set.all().count()
    comment_of_feed=feed_detail.comments_set.all().order_by('-pub_date')
    user_exp=feed_detail.users_experienced.all()
    user_concerned_list=feed_detail.user_concerns.all()
    for s in user_exp:
        print s
    
    img=[]
    pdf=[]
    doc=[]
    xls=[]
    audio=[]
    a=feed_detail.files
    b=feed_detail.files2
    c=feed_detail.files3
    for x in [a,b,c]:
        ext=os.path.splitext(x.name)[1]
        if ext in ['.jpeg','.jpg','.png',]:
            img.append(x)
        elif ext in ['.pdf']:
            pdf.append(x)
        elif ext in ['.docx','.doc']:
            doc.append(x)
        elif ext in ['.xlsx', '.xls']:
            xls.append(x)
        elif ext in ['.3gpp','.mp3']:
            audio.append(x)
    return render(request,'feed_detail.html' ,{'user_exp':user_exp,'audio':audio,'img':img,'pdf':pdf,'doc':doc,'xls':xls,'form':CommentsForm(),'feed_detail':feed_detail,'comment_of_feed':comment_of_feed,'comment_of_feed_count':comment_of_feed_count,'user_concerned_list':user_concerned_list})
   
from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from corrfeed.models import Feed


@login_required
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
 
@login_required 
@require_POST
def experience(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        feed = get_object_or_404(Feed, slug=slug)

        if feed.users_experienced.filter(id=user.id).exists():
            # user has already liked this company
            # remove like/user
            feed.users_experienced.remove(user)
        else:
            # add a new like for a company
            feed.users_experienced.add(user)

    ctx = {'likes_count': feed.total_experienced,}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json') 

@login_required
def post_comment(request,pk):
    form_class = CommentsForm
    feed_detail=get_object_or_404(Feed,pk=pk)
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.pub_date=timezone.now()
            comment.feed=get_object_or_404(Feed,pk=pk)
            comment.save()
            messages.success(request,'Comment successfully posted.')
            return redirect('feed_detail',slug=feed_detail.slug)
            #return render(request,'feed_detail.html',{'feed_detail':feed_detail})
           
    else:
        form = form_class()
        return render(request, 'feeed_detail.html', {'form': form,})     
 


from dal import autocomplete
class AuthorityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        #if not self.request.user.is_authenticated():
         #   return Country.objects.none()
        qs = Authority.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs
 
from chartit import DataPool,Chart
def chart(request,pk): 
    authority=get_object_or_404(Authority,pk=pk)
    authority.pub_date=timezone.now()
    authority.save()
    q=Authority.objects.filter(country=authority.country,category=authority.category).order_by('-pub_date')
    ds = DataPool(
       series=
        [{'options': {
            'source': q[:8]},
          'terms': [
            'name',
            'unresolved', 
            'resolved']}
         ])

    cht = Chart(
        datasource = ds, 
        series_options = 
          [{'options':{
              'type': 'column',
              'stacking': False},
            'terms':{
              'name': [
                'unresolved',
                'resolved']
              }}],
        chart_options = 
          {'title': {
               'text': 'Prissue.com Consumer Complaint Data for %s and similiar organizations'%authority.name},
           'xAxis': {
                'title': {
                   'text': '%s and similiar organizations'%authority.name}},
            'yAxis': {
                'title': {
                   'text': "Customer Issues"}}})
    return render(request,'organisation_stats.html',{'cht': cht})
    


def user_profile(request,username):
    user=get_object_or_404(User,username=username)    
    feeds=user.feeds.all()
    return render(request, 'user_profile.html' ,{'user':user,'feeds':feeds})