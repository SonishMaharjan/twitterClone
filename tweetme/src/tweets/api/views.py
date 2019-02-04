from tweets.models import Tweet
from rest_framework import generics
from django.db.models import Q
from .serializers import TweetModelSerializer

class TweetListAPIView(generics.ListAPIView):

    serializer_class= TweetModelSerializer

    def get_queryset(self, *args, **kwargs):
        qs = Tweet.objects.all()
        query = self.request.GET.get("q", None)
        print("query-------------->",query)
        if query is not None:
           qs = qs.filter(Q(content__icontains=query) |
                           Q(user__username__iexact=query)

                           )

        return qs