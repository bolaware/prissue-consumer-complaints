#-*-coding:utf-8-*-
from django.shortcuts import render,redirect
from corrfeed.models import Feed,Authority,Category
from django.utils import timezone
from django.db.models import Count
from django.shortcuts import render,get_object_or_404,render_to_response
from forms import FeedForm
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from  django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


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
    
def about(request):
    return render(request,'about.html')
    
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
    paginator = Paginator(feeds,10) # Show 25 contacts per page
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
    
'''def auth_card(request,pk,slug):
    authority=get_object_or_404(Authority,pk=pk)
    no_of_feed_per_authority=authority.feed_set.all().count()
    no_of_resolved_feed_per_authority=authority.feed_set.filter(resolved=True).count()
    if no_of_resolved_feed_per_authority==0:
        percent_resolved=0
    else:
        percent_resolved=(float(no_of_resolved_feed_per_authority) / no_of_feed_per_authority)*100
    
    return render(request, 'auth_card.html' , {'authority':authority,'no_of_feed_per_authority':no_of_feed_per_authority,'percent_resolved':percent_resolved})'''
    
def authority_details(request,pk,slug):
    user=request.user
    authority=get_object_or_404(Authority,pk=pk)
    feeds=authority.feed_set.all().order_by('-pub_date')
    no_of_feed_per_authority=authority.feed_set.all().count()
    no_of_resolved_feed_per_authority=authority.feed_set.filter(resolved=True).count()
    no_of_fllwrs=authority.following_orgs.all().count()
    p=False
    if bool(authority.dp)==False:
        p=True
    if no_of_resolved_feed_per_authority==0:
        percent_resolved=0
    else:
        percent_resolved=(float(no_of_resolved_feed_per_authority) / no_of_feed_per_authority)*100
    fl=False
    
    if user.is_authenticated():
        try:
            if bool(request.user.profile)==False:
                messages.success(request,'ERROR,Please update your profile first')
                return redirect('create-profile',username=user.username)
        except:
            pass
        profile=user.profile
        if profile.following_orgs.filter(id=authority.id).exists():
            fl=True
            
    
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
    'percent_resolved':percent_resolved,'no_of_fllwrs':no_of_fllwrs,'p':p,'fl':fl})
    

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

@login_required 
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
                messages.success(request,'Updated profile successfully.')
                #return HttpResponseRedirect(reverse('user_profile_submitted'))
                return redirect('home')
            else:
                form_errors = profile_formset.errors
                return render(request,'create_profile.html',{"form_errors":form_errors,"form": form,"profile_formset": profile_formset,})
    else:
        form = form_class(instance=userman)
        profile_formset = ProfileFormSet(instance=userman)
    return render(request,'create_profile.html',{"form": form,"profile_formset": profile_formset,})

@login_required 
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
    
    

@login_required   
def edit_feed(request,pk):
    feed=get_object_or_404(Feed,pk=pk)
    if feed.user != request.user:
        raise Http404
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
@login_required
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
    user_exp=feed_detail.users_experienced.all()
    user_concerned_list=feed_detail.user_concerns.all()
    f=False
    if request.user.saved.filter(id=feed_detail.id).exists():
        f=True
    
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
    return render(request,'feed_detail.html' ,{'f':f,'user_exp':user_exp,'audio':audio,'img':img,'pdf':pdf,'doc':doc,'xls':xls,'feed_detail':feed_detail,'user_concerned_list':user_concerned_list})
   
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
def follow_cat(request):
    try:
        if bool(request.user.profile)==False:
            messages.success(request,'ERROR,Update your profile before following!')
            return redirect('create-profile',username=user.username)
    except:
        pass
    if request.method == 'POST':
        print "--------------"
        profile = request.user.profile
        pk = request.POST.get('pk', None)
        category = get_object_or_404(Category,pk=pk)

        if profile.following_cats.filter(id=category.id).exists():
            # user has already liked this company
            # remove like/user
            profile.following_cats.remove(category)
            '''feed.user_concerns.remove(user)'''
            message = 'You unfollowed this category'
        else:
            # add a new like for a company
            profile.following_cats.add(category)
            ''''feed.user_concerns.add(user)'''
            message = 'You followed this category'

    ctx = {'name': category.name,'message': message,}
    return HttpResponse(json.dumps(ctx), content_type='application/json') 
    

@login_required 
@require_POST    
def follow_org(request):
    try:
        if bool(request.user.profile)==False:
            messages.success(request,'ERROR,Update your profile before following!')
            return redirect('create-profile',username=user.username)
    except:
        pass
    if request.method == 'POST':
        print "--------------"
        profile = request.user.profile
        pk = request.POST.get('pk', None)
        orgs = get_object_or_404(Authority,pk=pk)

        if profile.following_orgs.filter(id=orgs.id).exists():
            # user has already liked this company
            # remove like/user
            profile.following_orgs.remove(orgs)
            '''feed.user_concerns.remove(user)'''
            message = 'You unfollowed this organization'
        else:
            # add a new like for a company
            profile.following_orgs.add(orgs)
            ''''feed.user_concerns.add(user)'''
            message = 'You followed this organization'

    ctx = {'orgs': orgs.name,'message': message,}
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

    

'''@login_required 
@require_POST
def save(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        feed = get_object_or_404(Feed, slug=slug)

        if feed.archive.filter(id=user.id).exists():
            feed.archive.remove(user)
        else:
            feed.archive.add(user)

    ctx = {'likes_count': feed.total_experienced,}
    return HttpResponse(json.dumps(ctx), content_type='application/json') '''

@login_required   
def save(request,pk):
    feed=get_object_or_404(Feed,pk=pk)
    slug=feed.slug
    user=request.user
    if feed.archive.filter(id=user.id).exists():
        feed.archive.remove(user)
        messages.success(request,'You unsaved this post')
        print '--------------------'
    else:
        feed.archive.add(user)
        messages.success(request,'Added to your archive')
        print '--------------------'
    print '******************'
    return redirect('feed_detail',slug=slug)      
    
    
    
'''@login_required
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
        return render(request, 'feeed_detail.html', {'form': form,})     '''
 


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
    fb=False
    twitter=False
    linkedin=False
    try:
        if bool(user.profile.facebook)==True:
            fb=True
        if bool(user.profile.twitter)==True:
            twitter=True
        if bool(user.profile.linkedin)==True:
            linkedin=True
    except:
        pass
        
    paginator = Paginator(feeds,10) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        feedz = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        feedz = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        feedz = paginator.page(paginator.num_pages)
        
    return render(request, 'user_profile.html' ,{'fb':fb,'twitter':twitter,'linkedin':linkedin,'user':user,'feedz':feedz})
    
def category(request):
    if not request.user.is_authenticated():
        categories=Category.objects.all()
        return render(request,'category.html',{'categories':categories,})
                
    try:
        if bool(request.user.profile)==False:
            messages.success(request,'ERROR,Please update your profile first')
            return redirect('create-profile',username=user.username)
    except:
        pass
    categories=Category.objects.all()
    profile=request.user.profile
    fl=[]
    for category in categories:
        if profile.following_cats.filter(id=category.id).exists():
            fl.append(category)
    print fl
    
    return render(request,'category.html',{'categories':categories,'fl':fl}) 

def category_detail(request,slug):
    category=get_object_or_404(Category,slug=slug)
    a=Authority.objects.filter(category=category).count()
    fl=False
    if request.user.is_authenticated():
        try:
            if bool(request.user.profile)==False:
                messages.success(request,'ERROR,Please update your profile first')
                return redirect('create-profile',username=user.username)
        except:
            pass
        profile=request.user.profile
        if profile.following_cats.filter(id=category.id).exists():
            fl=True
    feeds=Feed.objects.filter(category_of_auth=category).order_by('-pub_date')
    paginator = Paginator(feeds,10) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        feedz = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        feedz = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        feedz = paginator.page(paginator.num_pages)
    
    return render(request,'category_detail.html',{'feeds':feeds,'a':a,'category':category,'feedz':feedz,'fl':fl})
    
    
def category_auth(request,slug):
    category=get_object_or_404(Category,slug=slug)
    authz=Authority.objects.filter(category=category)
    a=Authority.objects.filter(category=category).count()
    fl=False
    if request.user.is_authenticated():
        try:
            if bool(request.user.profile)==False:
                messages.success(request,'ERROR,Please update your profile first')
                return redirect('create-profile',username=user.username)
        except:
            pass
        profile=request.user.profile
        if profile.following_cats.filter(id=category.id).exists():
            fl=True
    
    paginator = Paginator(authz,10) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        auth= paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        auth = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        auth = paginator.page(paginator.num_pages)
    return render(request,'category_auth.html',{'a':a,'fl':fl,'category':category,'auth':auth})
    
def following(request,username):
    user=get_object_or_404(User,username=username)
    try:
        profile=user.profile
    except:
        messages.success(request,'ERROR,Please update your profile first')
        return redirect('create-profile',username=user.username)
    '''following_cats=profile.following_cats.all()   '''
    following_cats=Category.objects.all()
    following_orgs=profile.following_orgs.order_by('name') 
    fl=[]
    for category in following_cats:
        if profile.following_cats.filter(id=category.id).exists():
            fl.append(category)
    print fl    
    return render(request,'following.html',{'fl':fl,'following_orgs':following_orgs,'following_cats':following_cats})
    
@login_required   
def archive(request):
    feeds=request.user.saved.all().order_by('-pub_date')
    paginator = Paginator(feeds,10) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        feedz = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        feedz = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        feedz = paginator.page(paginator.num_pages)
    return render(request , 'archive.html' ,{'feedz':feedz})

import random    
def random_ten(request):
    num_feeds=Feed.objects.all().count()
    rand_feeds=random.sample(range(num_feeds),10)
    feeds=Feed.objects.filter(id__in=rand_feeds)
    return render(request,'random_ten.html',{'feeds':feeds}) 