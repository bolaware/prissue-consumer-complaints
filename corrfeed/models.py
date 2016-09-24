from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from validator import validate_file_extension
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver 
import os

class Country(models.Model):
    name=models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,editable=True)
    bio=models.TextField(max_length=300,blank=False)
    slug=models.SlugField(unique=True,editable=False)
    city=models.CharField(max_length=15,blank=True)
    country=models.ForeignKey(Country,null=True,blank=True)
    address=models.TextField(blank=True)
    '''phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], blank=True, max_length=16) # validators should be a list'''
    phone=PhoneNumberField(blank=True)
    
    @property    
    def full_name_of_user(self):
        return '%s %s'%(self.user.first_name,self.user.last_name)
            
    def save(self,*args,**kwargs):
       # a=Profile.objects.get(user=self.user)
        self.slug=slugify(self.user.username)
      #  a.save()
        super(Profile,self).save(*args,**kwargs)
    
    def __str__(self):
        return self.bio
        
class Category(models.Model):
    name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


'''def dp_filename(self,filename):
        url="files/dp/%s/%s"%(self.name)
        return url'''        


def dp_path(instance,filename):
    upload_dir=os.path.join('dp',instance.name) 
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir,filename)        

class Authority(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    country=models.ForeignKey(Country,null=True,blank=True)
    category=models.ForeignKey(Category,null=True,blank=True)
    slug=models.SlugField(editable=False)
    twitter_handle=models.CharField(max_length=30,blank=True,null=True)
    competitors=models.ManyToManyField("self",related_name="competitors",null=True,blank=True)
    no_of_feeds=models.PositiveIntegerField(default=0)
    resolved=models.PositiveIntegerField(default=0)
    unresolved=models.PositiveIntegerField(default=0)
    pub_date=models.DateTimeField(blank=True,null=True)
    dp = models.ImageField(blank=True,upload_to=dp_path)
    
    def save(self,*args,**kwargs):
        self.slug=slugify(unicode(self.name[:50]))
        n=1
        while Authority.objects.filter(slug=self.slug).exists():
            self.slug='%s-%d'%(self.slug,n)
            n+=1
        if bool(self.twitter_handle)==True:
            a=list(self.twitter_handle)
            if a[0] != '@':
                a=['@']+a
                self.twitter_handle="".join(a)
        
        super(Authority,self).save(*args,**kwargs)
        
       
        
        
        
    @property
    def total_feeds(self):
        a=Authority.objects.get(id=self.id)
        return a.feed_set.all().count()
        
    def __str__(self):
        return self.name
        
@receiver(models.signals.post_delete, sender=Authority)
def auto_delete_dp_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    x=instance.dp
    if x:
        if os.path.isfile(x.path):
            os.remove(x.path)


@receiver(models.signals.pre_save, sender=Authority)
def auto_delete_dp_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Authority.objects.get(pk=instance.pk).dp
    except Feed.DoesNotExist:
        return False

    new_file = instance.dp
    if old_file:
        if not old_file==new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    
    '''if old_files[0]:
        if not old_files[0]==new_files[0]:
            print 'IM HERE IM HERE IM HERE IM HERE IM HERE'
            if os.path.isfile(old_files[0].path):
                os.remove(old_files[0].path)'''


     
@receiver(post_save, sender = Authority)
def update_m2m_relationships(sender, **kwargs):
    if kwargs['created']: #only fire when creating new objects
        competitors_to_add = Authority.objects.filter(
                                country = kwargs['instance'].country,
                                category = kwargs['instance'].category
                                )
        for c in competitors_to_add:
            #c.competitors.add(kwargs['instance'])
            #c.save() #not creating a new object; this receiver does not fire here
            kwargs['instance'].competitors.add(c)
    elif not kwargs['created']:
        print '-------------------------------'
        current_competitors=kwargs['instance'].competitors.all()
        competitors_to_add = Authority.objects.filter(
                                country = kwargs['instance'].country,
                                category = kwargs['instance'].category
                                )
        for a in current_competitors:
            if a not in competitors_to_add:
                kwargs['instance'].competitors.remove(a)
        for a in competitors_to_add:
            if a not in current_competitors:
                kwargs['instance'].competitors.add(a)            
        
        
class Feed(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='feeds')
    text=models.TextField(blank=False,max_length=5000)
    user_concerns=models.ManyToManyField(User,related_name="likes",blank=True)
    users_experienced=models.ManyToManyField(User,related_name="experience",blank=True)
    pub_date=models.DateTimeField(blank=True,null=True)
    resolved=models.BooleanField(default=False)
    slug=models.SlugField(unique=True,editable=False)
    auth=models.ForeignKey(Authority,blank=False)
    #files=models.ForeignKey(FeedFiles,on_delete=models.CASCADE,related_name='files')
    files = models.FileField(upload_to="files/%Y/%m/%d",validators=[validate_file_extension])
    files2= models.FileField(upload_to="files/%Y/%m/%d",validators=[validate_file_extension],blank=True)
    files3= models.FileField(upload_to="files/%Y/%m/%d",validators=[validate_file_extension],blank=True)
    
    def get_absolute_url(self):
        return '/feeds/%s'%self.slug
    
    @property
    def no_of_comments(self):
        a=Feed.objects.get(pk=self.pk)
        return a.comments_set.all().count()    

    
    @property
    def total_concerns(self):
        return self.user_concerns.count()
    
    @property
    def total_experienced(self):
        return self.users_experienced.count()
        
    @property
    def attachment(self):
        attachment=0
        for x in [self.files,self.files2,self.files3]:
            if bool(x)==True:
                attachment+=1   
        return attachment               
            
    @property    
    def full_name_of_poster(self):
        return '%s %s'%(self.user.first_name,self.user.last_name)
        
    def publish(self):
        self.pub_date=timezone.now()
        self.save()
    
    def save(self,*args,**kwargs):
       # a=Profile.objects.get(user=self.user)
        self.slug=slugify(unicode(self.text[:50]))
        n=1
        while Feed.objects.filter(slug=self.slug).exists():
            self.slug='%s-%d'%(self.slug,n)
            n+=1
        
        super(Feed,self).save(*args,**kwargs)
        
        
    def __str__(self):
        return self.text

     
@receiver(post_save, sender = Feed)
def update_model_feed(sender, **kwargs):
    if kwargs['created']: #only fire when creating new objects
        kwargs['instance'].auth.no_of_feeds=kwargs['instance'].auth.feed_set.all().count()
        kwargs['instance'].auth.resolved=kwargs['instance'].auth.feed_set.filter(resolved=True).count()
        kwargs['instance'].auth.unresolved=kwargs['instance'].auth.feed_set.filter(resolved=False).count()
        kwargs['instance'].auth.save()
        print '******************************'
        #kwargs['instance'].save()
    elif not kwargs['created']:
        kwargs['instance'].auth.no_of_feeds=kwargs['instance'].auth.feed_set.all().count()
        kwargs['instance'].auth.resolved=kwargs['instance'].auth.feed_set.filter(resolved=True).count()
        print '-------------------------------'
        kwargs['instance'].auth.unresolved=kwargs['instance'].auth.feed_set.filter(resolved=False).count()
        kwargs['instance'].auth.save()
        #kwargs['instance'].save()
 
# These two auto-delete files from filesystem when they are unneeded:
@receiver(models.signals.post_delete, sender=Feed)
def auto_delete_feed_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    for x in [instance.files,instance.files2,instance.files3]:
        if x:
            if os.path.isfile(x.path):
                os.remove(x.path)

@receiver(models.signals.pre_save, sender=Feed)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is changed.
    """
    
    if not instance.pk:
        return False

    try:
        old_file = Feed.objects.get(pk=instance.pk).files
        old_file2 = Feed.objects.get(pk=instance.pk).files2
        old_file3 = Feed.objects.get(pk=instance.pk).files3
        old_files=[old_file,old_file2,old_file3]
    except Feed.DoesNotExist:
        return False

    new_file = instance.files
    new_file2=instance.files2
    new_file3=instance.files3
    new_files=[new_file,new_file2,new_file3]
    
    if old_files[0]:
        if not old_files[0]==new_files[0]:
            print 'IM HERE IM HERE IM HERE IM HERE IM HERE'
            if os.path.isfile(old_files[0].path):
                os.remove(old_files[0].path)
    if old_files[1]:        
        if not old_files[1]==new_files[1]:
            if os.path.isfile(old_files[1].path):
                os.remove(old_files[1].path)
    if old_files[2]:
        if not old_files[2]==new_files[2]:
            if os.path.isfile(old_files[2].path):
                os.remove(old_files[2].path)
    
    
    '''if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)'''

class Comments(models.Model):
    text=models.TextField(blank=False,max_length=150)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    feed=models.ForeignKey(Feed,blank=True)      
    pub_date=models.DateTimeField(blank=True,null=True)
    
    def publish(self):
        self.pub_date=timezone.now()
        self.save()
    
    @property    
    def full_name_of_poster(self):
        return '%s %s'%(self.user.first_name,self.user.last_name)
        
    def __str__(self):
        return self.text

        

    
        



