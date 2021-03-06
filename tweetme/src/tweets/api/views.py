from tweets.models import Tweet
from rest_framework import generics
from django.db.models import Q
from .serializers import TweetModelSerializer

from rest_framework import permissions
from .pagination import StandardResultsPagination


class TweetCreateAPIView(generics.CreateAPIView):
    serializer_class = TweetModelSerializer
    permission_classes=[permissions.IsAuthenticated,]
    #called when newcdata is saved in db
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class TweetListAPIView(generics.ListAPIView):

    serializer_class= TweetModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        #profile is related_name in UserProfile model
        print(self.request.user)
        im_following = self.request.user.profile.get_following()
        qs1 = Tweet.objects.filter(user__in=im_following)
        qs2 =Tweet.objects.filter(user=self.request.user)
        #distinct remove duplicate
        qs=(qs1|qs2).distinct().order_by("-timestamp")
        query = self.request.GET.get("q", None)
        print("query-------------->",query)
        if query is not None:
           qs = qs.filter(Q(content__icontains=query) |
                           Q(user__username__iexact=query)

                           )


        return qs
