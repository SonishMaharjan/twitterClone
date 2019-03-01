from rest_framework import serializers
from tweets.models import Tweet
from accounts.api.serializers import UserDisplaySerializer

from django.utils.timesince import timesince




class ParentTweetModelSerializer(serializers.ModelSerializer):
    #dount show user input in create form if read_only = True
    user =UserDisplaySerializer(read_only=True)

    #you use value.date_display in listView ajax part
    date_display =serializers.SerializerMethodField()
    timesince= serializers.SerializerMethodField()


    class Meta:
        model=Tweet
        fields = ["id","user","content","timestamp","date_display","timesince"]


    def get_date_display(self,obj):
        return obj.timestamp.strftime("%b %d, %Y @ %I:%M %p ")
    def get_timesince(self,obj):
        return timesince(obj.timestamp) + " ago"


class TweetModelSerializer(serializers.ModelSerializer):
    #dount show user input in create form if read_only = True
    user =UserDisplaySerializer(read_only=True)
    #you use value.date_display in listView ajax part
    date_display =serializers.SerializerMethodField()
    timesince= serializers.SerializerMethodField()
    #parent should be atrrtibuet of Tweet in tweet modeels
    parent= ParentTweetModelSerializer(read_only=True)

    class Meta:
        model=Tweet
        fields = ["id","user","content","timestamp","date_display","timesince","parent"]

    def get_is_retweet(self,obj):
        if obj.parent:
            return True
        else:
            return False
    def get_date_display(self,obj):
        return obj.timestamp.strftime("%b %d, %Y @ %I:%M %p ")
    def get_timesince(self,obj):
        return timesince(obj.timestamp) + " ago"
