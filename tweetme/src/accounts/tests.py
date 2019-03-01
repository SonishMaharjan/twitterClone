from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.

from .models import UserProfile

User=get_user_model()

class UserProfileTestCase(TestCase):
    ##i was doing test

    def setUp(self):
        self.username= "some_user"
        new_user = User.objects.create(username=self.username)
    # start function name with test_...
    def test_user_profile(self):
        username = self.username

        user_profile = UserProfile.objects.filter(user__username=self.username)
        self.assertTrue(user_profile.exists())
        self.assertTrue(user_profile.count()==1)

    def test_new_user(self):
        #same as in setup soo.. gives error
        new_user = User.objects.create(username=self.username+"s")
