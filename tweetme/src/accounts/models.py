from django.db import models
from django.conf import settings
# Create your models here.
from django.db.models.signals import post_save

from tweets.models import Tweet


class UserProfileManager(models.Manager):
    use_for_related_fields=True

    def all(self):
        qs = self.get_queryset().all()
        #excludin following by same user to self
        try:
            if self.instance:
                qs= qs.exclude(user=self.instance)
        except:
            pass
        # print(self)
        # print(dir(self))
        # print(self.instance)
        return qs

    #manage follow/ unfollow users
    def toggle_follow(self,user,to_toggle_user):
        user_profile,created = UserProfile.objects.get_or_create(user=user)

        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            isFollowed = False
        else:
            user_profile.following.add(to_toggle_user)
            isFollowed=True
        return isFollowed
    def is_following(self,user,followed_by_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False


class UserProfile(models.Model):
    #model.OneToOneField(modelName,)
    #related_name is used in template
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='profile',on_delete=models.CASCADE)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="followed_by")

    objects = UserProfileManager()

    def __str__(self):
        #return str(self.following.all().count())
        return str(self.user)

    def get_following(self):
        users =self.following.all() #Users.obhects.all()
        return users.exclude(username=self.user.username)

def  post_save_user_receiver(sender,instance,created,*args,**kwargs):

    #print(instance)
    if created:
        new_profile = UserProfile.objects.get_or_create(user=instance)

        #celery + redis
        #do some email task after user sign up

#post_save.connect(post_save_user_receiver,sender=Model)
#when new user is connected it will also be added in UserProfile
post_save.connect(post_save_user_receiver,sender=settings.AUTH_USER_MODEL)
