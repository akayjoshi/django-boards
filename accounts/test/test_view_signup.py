from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from ..views import signup
from ..forms import SignUpForm
# from django.contrib.auth.forms import UserCreationForm i'm running this and it runs with this


# Create your tests here.
class SignUpTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.res = self.client.get(url) # res should be in self so it will be accessible.

    def test_signup_status_code(self):
        self.assertEquals(self.res.status_code, 200)

    def test_signup_resolve_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEquals(view.func, signup)
    
    def test_csrf(self):
        self.assertContains(self.res, 'csrfmiddleware')

    def test_contain_form(self):
        form = self.res.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        self.assertContains(self.res, '<input', 5)
        self.assertContains(self.res, 'type="text"', 1)
        self.assertContains(self.res, 'type="email"', 1)
        self.assertContains(self.res, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
    
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'aju',
            'email': 'ajay@gmail.com', #test can run without this because signupform is inherited by usercreationform 
            'password1': 'jai@aj123',
            'password2': 'jai@aj123'
        }
        self.res = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirection(self):
        self.assertRedirects(self.res, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        res = self.client.get(self.home_url)
        user = res.context.get('user')
        self.assertTrue(user.is_authenticated)

        
class InvalidSignUpTest(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_invalid_data_dont_create_user(self):
        self.assertFalse(User.objects.exists())

    def test_contains_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
