from django.db import models
from django.conf import settings
#editable time to show in admin panel
#from django.utils import timezone
from .validators import validate_content
# Create your models here.
from django.urls import reverse,reverse_lazy

class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    content= models.CharField(max_length=255,validators=[validate_content,])
    #is updated when object is updated
    updated= models.DateTimeField(auto_now = True)
    #can not be update
    timestamp = models.DateTimeField(auto_now_add= True)
    #editable time showing in admin panel
    #created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content

    #it is also called by object.get_absolute_url in template see tweet_list.html
    def get_absolute_url(self):
        return reverse_lazy("tweets:detail_view",kwargs={"pk":self.pk})
