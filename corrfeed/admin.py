

from django.contrib import admin
from .models import Profile,Feed,Authority

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display=('full_name_of_user' ,'bio','country','slug')
 #   prepopulated_fields={'slug':('user',)}
    
class FeedAdmin(admin.ModelAdmin):
    model = Feed
    list_display=('text','full_name_of_poster','resolved','total_concerns','auth')
    
class AuthorityAdmin(admin.ModelAdmin):
    model = Authority
    list_display=('name','description','total_feeds')

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Feed,FeedAdmin)
admin.site.register(Authority,AuthorityAdmin)

