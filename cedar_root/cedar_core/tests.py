




from django.test import TestCase, SimpleTestCase
from django.urls import reverse


# python .\cedar_root\manage.py test cedar_core
# $ ./manage.py test --settings=settings.unittest


class IndexViewTest(SimpleTestCase):

    case_test_URL = '/'
    case_test_URL_name = 'index'
    case_test_template =  'cedar_site/index.html'

    # Test Get
    def test_view_get(self):
        response = self.client.get(self.case_test_URL)
        self.assertEqual(response.status_code, 200)

    # Test Get by Name
    def test_view_get_by_name(self):
        response = self.client.get(reverse(self.case_test_URL_name))
        self.assertEqual(response.status_code, 200)

    # Test Template
    def test_view_get_template(self):
        response = self.client.get(reverse(self.case_test_URL_name))
        self.assertTemplateUsed(response, self.case_test_template)



class AuthViewsTest(SimpleTestCase):

    def test_view_get(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)

