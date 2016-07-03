from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from validator import validate_file_extension
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profiles')
    bio=models.TextField(max_length=300,blank=False)
    slug=models.SlugField(unique=True,editable=False)
    city=models.CharField(max_length=15,blank=True)
    country=models.CharField(max_length=15,blank=True)
    
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
        
class Authority(models.Model):
    name=models.CharField(max_length=100,blank=False)
    description=models.TextField(max_length=2000,blank=False)
    
    def __str__(self):
        return self.name
        
class Authority(models.Model):
    name=models.CharField(max_length=100,blank=False)
    description=models.TextField(max_length=2000,blank=False)
    
    def __str__(self):
        return self.name
        
        
    @property
    def total_feeds(self):
        a=Authority.objects.get(name=self.name)
        return a.feed_set.all().count()
        

class Feed(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='feeds')
    text=models.TextField(blank=False,max_length=500)
    user_concerns=models.ManyToManyField(User,related_name="likes",blank=True)
    pub_date=models.DateTimeField(blank=True,null=True)
    resolved=models.BooleanField(default=False)
    slug=models.SlugField(unique=True,editable=False)
    auth=models.ForeignKey(Authority,blank=False)
    files = models.FileField(upload_to="files/%Y/%m/%d", validators=[validate_file_extension])
    
        
    @property
    def total_concerns(self):
        return self.user_concerns.count()
    
    
    @property    
    def full_name_of_poster(self):
        return '%s %s'%(self.user.first_name,self.user.last_name)
        
    def publish(self):
        self.pub_date=timezone.now()
        self.save()
    
    def save(self,*args,**kwargs):
       # a=Profile.objects.get(user=self.user)
        self.slug=slugify(self.text)
      #  a.save()
        super(Feed,self).save(*args,**kwargs)   
     
    def __str__(self):
        return self.text
        

        
        

        

    
        



