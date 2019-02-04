
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserDisplaySerializer(serializers.ModelSerializer):
    #gets value thruogh a function (mehtod name) by deafault get_follower_count()
    follower_count = serializers.SerializerMethodField(method_name="hawa")
    class Meta:
        model=User
        fields=[
            "username",
            "first_name",
            "last_name",
            "follower_count",

        ]

    def hawa(self,obj):
        #print(obj.username)
        return 5