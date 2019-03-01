from django.forms.utils import ErrorList
from django import forms

#inherits form object class in py<v3  FormUserNeededMixin(object) after v3  FormUserNeededMixin() is fine
class FormUserNeededMixin():
    
    #this class is inherited on TreatCreateView so when form_valid is called during submission this is called
    def form_valid(self,form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super(FormUserNeededMixin,self).form_valid(form)
        else:
            form._errors[forms.forms.NON_FIELD_ERRORS]=ErrorList(["User le must logged in to continue."])
            return self.form_invalid(form)

#make sure that user can only update their tweet
class UserOwnMixin():
    def form_valid(self,form):


        #form.instance.user is user in form
        if form.instance.user == self.request.user:
            return super().form_valid(form)
        else:
            form._errors[forms.forms.NON_FIELD_ERRORS]=ErrorList(["This user  can not edit this tweet."])
            return self.form_invalid(form)
