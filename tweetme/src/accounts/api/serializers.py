
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.urls import reverse_lazy

User = get_user_model()

class UserDisplaySerializer(serializers.ModelSerializer):
    #gets value thruogh a function (mehtod name) by deafault get_follower_count()
    follower_count = serializers.SerializerMethodField(method_name="hawa")
    url = serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=[
            "username",
            "first_name",
            "last_name",
            "follower_count",
            "url"

        ]

    def hawa(self,obj):
        #print(obj.username)
        return 5

    def get_url(self,obj):
        #reverse_lazy("url_namespace:url_name")
        return reverse_lazy("accounts:detail_view",kwargs={"username":obj.username})
