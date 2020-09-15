from django.test import TestCase
from account.models import User

# Create your tests here.


class UserTests(TestCase):

    def test_user(self):
        """Test case to test making a simple user"""

        user = User.objects.create_user(username='afaq2', password='admin')
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.is_anonymous, False)
        self.assertEqual(user.is_admin, False)

    def test_superuser(self):
        """Test case to test the admin user creating"""

        user = User.objects.create_superuser(username='afaq1', password='admin')
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_admin, True)



