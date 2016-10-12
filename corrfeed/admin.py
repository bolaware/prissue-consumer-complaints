

from django.contrib import admin
from .models import Profile,Feed,Authority,Country,Category

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display=('full_name_of_user' ,'bio','country','slug')
 #   prepopulated_fields={'slug':('user',)}
    
class FeedAdmin(admin.ModelAdmin):
    model = Feed
    list_display=('text','full_name_of_poster','resolved','total_concerns','auth')
    
class CountryAdmin(admin.ModelAdmin):
    model = Country
    list_display=('name',)
    
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display=('name',)
    
class AuthorityAdmin(admin.ModelAdmin):
    model = Authority
    list_display=('name','description','total_feeds')
    
'''class CommentsAdmin(admin.ModelAdmin):
    model = Comments
    list_display=('text','user','feed')'''
    



admin.site.register(Profile,ProfileAdmin)
admin.site.register(Feed,FeedAdmin)
admin.site.register(Authority,AuthorityAdmin)
admin.site.register(Country,CountryAdmin)
admin.site.register(Category,CategoryAdmin)