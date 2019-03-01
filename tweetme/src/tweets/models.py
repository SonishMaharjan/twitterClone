from django.db import models
from django.conf import settings
#editable time to show in admin panel
#from django.utils import timezone
from .validators import validate_content
# Create your models here.
from django.urls import reverse,reverse_lazy

from django.utils import timezone


class TweetManager(models.Manager):

    def retweet(self,user,parent_obj):
        if parent_obj.parent:
            og_parent=parent_obj.parent
        else:
            og_parent= parent_obj
        # print("11")
        # print(self.get_queryset())
        # print("22")
        # print(self.get_queryset().filter(user=user,parent=parent_obj))
        qs = self.get_queryset().filter(user=user,parent=og_parent).filter(
        timestamp__year = timezone.now().year,
        timestamp__month = timezone.now().month,
        timestamp__day = timezone.now().day,
        )
        #print(qs)
        if qs.exists():
            return None
        print(" is the user")
        print(user)
        obj= self.model(
            parent = parent_obj,
            user = user,
            content = parent_obj.content,
        )
        obj.save()
        return obj

class Tweet(models.Model):
    parent = models.ForeignKey("self",blank=True,null=True,on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    content= models.CharField(max_length=255,validators=[validate_content,])
    #is updated when object is updated
    updated= models.DateTimeField(auto_now = True)
    #can not be update
    timestamp = models.DateTimeField(auto_now_add= True)
    #editable time showing in admin panel
    #created_at = models.DateTimeField(default=timezone.now)

    #objects is called in retweet view
    objects= TweetManager()

    class Meta:
        ordering=['-timestamp',]

    def __str__(self):
        return self.content

    #it is also called by object.get_absolute_url in template see tweet_list.html
    def get_absolute_url(self):
        return reverse_lazy("tweets:detail_view",kwargs={"pk":self.pk})
