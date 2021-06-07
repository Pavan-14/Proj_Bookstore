from django.test import TestCase

class ViewsTestCase(TestCase):
    
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('http://3.85.22.38:8080/books/')
        self.assertEqual(response.status_code, 200)
    
    def test_login(self):
        response = self.client.get('http://3.85.22.38:8080/cuser/signin/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cuser/signin.html')
