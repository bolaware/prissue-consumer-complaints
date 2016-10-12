from django.forms import ModelForm
from models import Feed,Authority,Profile,Country,Category
from django.contrib.auth.models import User
from dal import autocomplete
from django import forms

class FeedForm(ModelForm):
    class Meta:
        model=Feed
        fields=('text','auth','files','files2','files3')
        widgets={"files":forms.FileInput(attrs={'id':'files','required':True, }),
                 "text":forms.Textarea(attrs={'rows':5,'class':"mdl-textfield__input",'id':'text','required':True,'type':'text',}),
                 #"auth":forms.Select(attrs={'class':"mdl-select__input",'id':'auth','required':True,'name':'auth'})
                 'auth': autocomplete.ModelSelect2(url='authority-autocomplete',attrs={'data-minimum-input-length': 2,'data-placeholder': 'Search Organization...','required':True})}
                 
       
        
'''widgets={
                      "name":forms.TextInput(attrs={'placeholder':'Name','name':'Name','id':'common_id_for_imputfields','class':'input-class_name'}),
                      "description":forms.TextInput(attrs={'placeholder':'description','name':'description','id':'common_id_for_imputfields','class':'input-class_name'})'''


        
class EditFeedForm(ModelForm):
    class Meta:
        model=Feed
        fields=('text','resolved','files','files2','files3')
        widgets={ "text":forms.Textarea(attrs={'rows':8,'class':"mdl-textfield__input",'id':'text','required':True,'type':'text',}),
                  "resolved":forms.CheckboxInput(attrs={"id":"checkbox","type":"checkbox","class":"mdl-checkbox__input",}),}

from django.forms.models import inlineformset_factory        
class UserForm(ModelForm):
    class Meta:
        model=User
        fields=('first_name','last_name',)
        widgets={ "first_name":forms.TextInput(attrs={'class':"mdl-textfield__input",'required':True,'id':'first_name','type':'text',}),
                  "last_name":forms.TextInput(attrs={'class':"mdl-textfield__input",'required':True,'id':'last_name','type':'text',}),}  
   
        
ProfileFormSet = inlineformset_factory(User,Profile,can_delete=False,fields=('bio','city','country','address','phone','facebook','twitter','linkedin'),widgets={ "bio":forms.Textarea(attrs={'class':"mdl-textfield__input",'id':'text','required':True,'rows':3,'type':'text',}),
           "city":forms.TextInput(attrs={'class':"mdl-textfield__input",'id':'city','type':'text',}),
           "address":forms.Textarea(attrs={'class':"mdl-textfield__input",'id':'address','type':'text',}),
           "facebook":forms.TextInput(attrs={'class':"mdl-textfield__input",'id':'facebook','type':'text',}),
           "twitter":forms.TextInput(attrs={'class':"mdl-textfield__input",'id':'twitter','type':'text',}),
           "linkedin":forms.TextInput(attrs={'class':"mdl-textfield__input",'id':'linkedin','type':'text',}),
           "phone":forms.TextInput(attrs={'class':"mdl-textfield__input",'id':'phone','type':'text',}),} ) 
           


class AuthorityForm(ModelForm):
    class Meta:
        
        model=Authority
        fields=('name','description','country','category','twitter_handle','dp',)
        widgets={"name":forms.TextInput(attrs={'class':"mdl-textfield__input",'id':'Name','required':True, }),
                 "category":forms.Select(attrs={'required':True, }),
                 "country":forms.Select(attrs={'required':True, }),
                 "description":forms.Textarea(attrs={'columns':10,'rows':5,'class':"mdl-textfield__input",'id':'note','required':True,'type':'text',}),
                 "twitter_handle":forms.TextInput(attrs={'columns':10,'class':"mdl-textfield__input",'id':'Name', })}
    
class EditAuthorityForm(ModelForm):
    class Meta:
        model=Authority
        fields=('name','description','country','category','twitter_handle',)
        
'''class EditAuthDpForm(ModelForm):
    class Meta:
        model=Authority
        fields=('dp',)'''
        
from allauth.account.forms import LoginForm,BaseSignupForm,SignupForm

class MyLoginForm(LoginForm):
    def __init__(self,*args,**kwargs):
        super(MyLoginForm,self).__init__(*args,**kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'class':"mdl-textfield__input",'required':True,})
        self.fields['password'].widget=forms.PasswordInput(attrs={'class':"mdl-textfield__input",'required':True,})
        self.fields['remember'].widget=forms.CheckboxInput(attrs={'class':"mdl-checkbox__input",})
 
 
 
class MySignupForm(SignupForm) :
    def __init__(self,*args,**kwargs):
        super(SignupForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget= forms.TextInput(attrs={'class':"mdl-textfield__input",'required':True,})
        self.fields['email'].widget=forms.TextInput(attrs={'class':"mdl-textfield__input",'required':True,})
        self.fields['password1'].widget=forms.PasswordInput(attrs={'pattern':'(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$','class':"mdl-textfield__input",'required':True,})
        self.fields['password2'].widget=forms.PasswordInput(attrs={'class':"mdl-textfield__input",'required':True,})

