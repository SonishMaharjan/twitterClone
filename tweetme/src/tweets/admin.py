from django.contrib import admin

from .models import Tweet
from .forms import TweetModelForm
# Register your models here.

admin.site.register(Tweet)

#use this to edit admin form
# class TweetModelAdmin(admin.ModelAdmin):
#     form = TweetModelForm
#
# admin.site.register(Tweet,TweetModelAdmin)
