from django.test import TestCase
from django.urls import reverse
from ..models import User
from config.my_module.my_test_module import create_user, assert_normal_get_request, redirect_dashboard


# Tests
class LoginViewTests(TestCase):
    """LoginViewのテスト"""

    # 正常値
    def test_normal_login_request(self):
        """LoginView: 正常値"""
        url = reverse('accounts:login')
        # assert get method
        assert_normal_get_request(self, url)
        # redirect dashboard
        redirect_dashboard(self, url)


class LogoutViewTests(TestCase):
    """LogoutViewのテスト"""

    # create user
    def setUp(self):
        create_user(self)

    # 正常値
    def test_logout_request(self):
        """LogoutViewのテスト"""
        # assert logout
        url = reverse('accounts:logout')
        assert_normal_get_request(self, url, status_code=302)
        # assert redirect
        self.client.login(username='test_user', password='password')
        response = self.client.get(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('notepad:home'))
        


class SignupViewTests(TestCase):
    """SignupViewのテスト"""

    # 正常値
    def test_normal_siginup_request(self):
        """SignupView: 正常値"""
        url = reverse('accounts:signup')
        # assert get method
        assert_normal_get_request(self, url)
        # redirect dashboard
        redirect_dashboard(self, url)


class ProfileUpdateViewTests(TestCase):
    """ProfileUpdateViewのテスト"""

    # create user
    def setUp(self):
        create_user(self)

    # 正常値
    def test_normal_get_request(self):
        """ProfileUpdateView: 正常値"""
        # url variable
        url = reverse('accounts:profile', kwargs={'pk': self.user.id})
        # assert get method
        assert_normal_get_request(self, url)


class FollowViewTests(TestCase):
    """FollowViewのテスト"""

    # 正常値
    def test_normal_value_view(self):
        """FollowView: 正常値"""
        # create user
        create_user(self)
        follow_user = User.objects.create_user('follow_test', password='follow_test')
        self.client.login(username='test_user', password='password')
        # get request
        kwargs = {
            'following': self.user.pk,
            'followed': follow_user.pk,
        }
        url = reverse('accounts:follow', kwargs=kwargs)
        assert_normal_get_request(self, url, status_code=302)
        # check redirect
        redirect_url = reverse('notepad:dashboard', kwargs={'pk': follow_user.pk})
        resp = self.client.get(url)
        self.assertRedirects(resp, redirect_url)
        # check follow
