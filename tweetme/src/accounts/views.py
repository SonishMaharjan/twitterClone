from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect
from .models import UserProfile

# Create your views here.
User = get_user_model()

class UserDetailView(DetailView):
    #queryset = User.objects.all()
    template_name = "accounts/user_detail.html"

    #return the single object this view will display
    #either queryset of get_queryset is used as source
    def get_object(self):

        return get_object_or_404(User,username__iexact=self.kwargs.get("username"))

    def get_context_data(self,*args,**kwargs):
        context =super(UserDetailView,self).get_context_data(*args,**kwargs)
        # print(args)

        # print(dir(self))
        # print(self.kwargs)
        # print(kwargs)
        # print(UserProfile.objects.get(user__username=kwargs.get("object")))
        context["following"] = UserProfile.objects.is_following(self.request.user,self.get_object())
        return context



class UserFollowView(View):
    #Not  confuse with Model.objects.get(id=3) its get from View
    #its get Http method
    def get(self,request,username,*args,**kwargs):
        #toggle_user = get_object_or_404(User,username__iexact=kwargs.get("username"))
        #print(username)
        toggle_user = get_object_or_404(User,username__iexact=username)
        if request.user.is_authenticated:
            is_following=UserProfile.objects.toggle_follow(request.user,toggle_user)

        return redirect("accounts:detail_view",username=username)

        #same as
        #url = reverse("accounts:detail_view",kwargs={"username":username})
        #HttpResponseRedirect(url)
