# from django.contrib.auth.models import AnonymousUser, User
# from cuser.views import user_signingit 
from django.test import TestCase, RequestFactory
from django.test import Client

class ViewsTestCase(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.factory = RequestFactory()
   
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('http://3.85.22.38:8080/books/')
        self.assertEqual(response.status_code, 200)
  
    def test_login(self):
        response = self.client.get('http://3.85.22.38:8080/cuser/signin/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cuser/signin.html')

    # def test_login(self):
    #     request = self.factory.get('http://3.85.22.38:8080/cuser/signin/')
    #     request.user = AnonymousUser()
    #     response = user_signin(request)

    #     self.assertNotEqual(response.status_code, 404, 'status code not 404')