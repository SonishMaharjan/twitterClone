from django.shortcuts import render
from .models import Tweet
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin,UserOwnMixin
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse

from django.forms.utils import ErrorList
from django import forms

from django.db.models import Q

#pok is set from url ?P<pok>
def tweet_detail_view(request,pok=None):
    #print(pok)

    #both id and pok works fine
    #obj = Tweet.objects.get(pk=pok)
    obj = Tweet.objects.get(id=pok)
    context= {
        "object":obj,
    }
    return render(request,"tweets/detail_view.html",context)

def tweet_list_view(request):
    queryset = Tweet.objects.all()
    context = {
    "objects":queryset
    }

    return render(request,"tweets/list_view.html",context)

def tweet_create_view(request):
    form = TweetModelForm(request.POST or None)
    #we tkaing user who post the tweet
    if form.is_valid():
        #use this to manually set any fields:
        instance  = form.save(commit=False)
        #print(instance)
        instance.user = request.user
        instance.save()
    context = {
        "form":form
    }

    return render(request,"tweets/tweet_form.html",context)


#class base view
class TweetDetailView(DetailView):
    #if template name is not given it looks for tweet_detail.html
    template_name = "tweets/detail_view.html"
    #refer result of this by object variralbe in .html file.. notice not return of context here
    def get_object(self):
        #print(self.kwargs)
        #pk = self.kwargs.get("pk")
        return Tweet.objects.get(id=self.kwargs["pk"])

class TweetListView(ListView):
    #tweet_list.html is default
    #template_name= "tweets/list_view.html"
    #the output of queryset is default stored in "object_list"/"tweet_list"(tweet from model name)
    # variable and can be used in .html file or use get_context_data gfxn
    #queryset = Tweet.objects.all()
    def get_queryset(self,*args,**kwargs):
        qs =Tweet.objects.all()

        #QueryDict.get("q",default=None) returns default value none whent key 'q' not found
        #print(self.request.GET.get("q",None))
        query= self.request.GET.get("q",None)
        #print(query)
        if query is not None:
            #qs = qs.filter(content__icontains=query|user__username__icontains=query)

            #qs = qs.filter(content__icontains=query).filter(user__username__icontains=query)
            # qs = qs.filter(user__username__icontains=query)
            qs =qs.filter(Q(content__icontains=query)|
                            Q(user__username__iexact=query)

                            )


           # print(qs)
        #print(qs)
        return qs

    #adding key for context so you can use it in template
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        #add your custom context here
        #context["custom_list"] = Tweet.objects.all()
        context["custom_list"]=self.get_queryset(*args,**kwargs)
        context["create_form"]= TweetModelForm()
        context["create_redirect_url"] = reverse_lazy("tweets:create_view")
        #print(type(context))
        #print(context)
        return context



class TweetCreateView(LoginRequiredMixin,FormUserNeededMixin,CreateView):
    form_class= TweetModelForm
    template_name = "tweets/tweet_form.html"
    #cant do here got a problem while passing pk so done in get_absolute_url in TweetModel
    #success_url = reverse_lazy("tweets:detail_view",kwargs={"pk":object.getKey("pk")})

    login_url ="/admin/"

    # model Form use form_valid, also to save data so if any change in field value needed modify here
    # def form_valid(self,form):
    #   # is called when form is posted
            #shoul return HttpResponse
    #
    #     form.instance.user = self.request.user
    #     #return super(TweetCreateView,self).form_valid(form) #old python way
    #     return super().form_valid(form)

    #not showin error when user is not logged in while posting tweet and later moved to mixins.py
    # def form_valid(self,form):
    #     if self.request.user.is_authenticated():
    #         form.instance.user = self.request.user
    #         return super(TweetCreateView,self).form_valid(form)
    #     else:
    #         form._errors[forms.forms.NON_FIELD_ERRORS]=ErrorList(["User must logged in to continue."])
    #         return self.form_invalid(form)

class TweetUpdateView(LoginRequiredMixin,UserOwnMixin,UpdateView):
    queryset = Tweet.objects.all()
    form_class = TweetModelForm
    template_name = "tweets/tweet_update.html"
    success_url ="/tweets/"

class TweetDeleteView(FormUserNeededMixin,UserOwnMixin,DeleteView):
    template_name = "tweets/tweet_delete.html"
    model = Tweet
    #send name=list_view in url url.py
    success_url = reverse_lazy("tweets:list_view")
