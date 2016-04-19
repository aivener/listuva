from django.test import TestCase
from django.core.urlresolvers import reverse_lazy, reverse
from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.messages import get_messages
import datetime
from datetime import date, time
from django.http import HttpResponse

from django.http import JsonResponse
import json


class CoverageTests(TestCase):
    def test_maketable(self):
        response = self.client.get('http://expul:8000/api/v1/maketable')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        self.assertEqual(len(deser), 3)


    def test_getallcatname(self):
        response = self.client.get('http://expul:8000/api/v1/getallcatname/')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        num_cats = len(deser)
        self.assertEqual(num_cats, 3)


    def test_create_listing_exp_api(self):
        response = self.client.get('http://expul:8000/api/v1/postbycat/1')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        numPosts = len(deser)

        url = 'http://expul:8000/api/v1/create_listing_exp_api/'
        response = self.client.post(url,
                                    {'category': '1',
                                     'subcategory': '2',
                                     'title': 'Creating',
                                     'summary': 'Test Posting',
                                     'price': '1.23',
                                     'auth': 123,
                                     })
        # response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
                'http://expul:8000/api/v1/search/',
                {'searchText': 'Creating'}
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get('http://expul:8000/api/v1/postbycat/1')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        newnumPosts = len(deser)
        self.assertEqual(newnumPosts, numPosts+1)

    def test_get_posts_by_category(self):
        response = self.client.get('http://expul:8000/api/v1/postbycat/1')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))

    def test_get_posts_by_subcategory(self):
        response = self.client.get('http://expul:8000/api/v1/postbysubcat/1')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))

        response = self.client.get('http://expul:8000/api/v1/postbysubcat/2')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))

    def test_getcatname(self):
        response = self.client.get('http://expul:8000/api/v1/getcatname/1')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))

    def test_getSubcatName(self):
        response = self.client.get('http://expul:8000/api/v1/getsubcatname/1')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))

    def test_getAllSubCatName(self):
        response = self.client.get('http://expul:8000/api/v1/getallsubcatname/')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))

    def test_getCatNameFromSubcat(self):
        response = self.client.get('http://expul:8000/api/v1/catname/1')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        response = self.client.get('http://expul:8000/api/v1/catname/7')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))

    def test_login_exp_api(self):
        response = self.client.get('http://expul:8000/api/v1/login_exp_api/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            'http://expul:8000/api/v1/login_exp_api/',
            {'email': 'mdh3hc@virginia.edu', 'password': 'hello' }
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            'http://expul:8000/api/v1/login_exp_api/',
            {'email': 'mdh3hc123@virginia.edu', 'password': 'hello' }
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            'http://expul:8000/api/v1/login_exp_api/',
            {'email': 'yo@yo.com', 'password': 'yo' }
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            'http://expul:8000/api/v1/login_exp_api/',
            {'email': '123', 'password': 'yo' }
        )
        self.assertEqual(response.status_code, 200)

    def test_getPost(self):
        response = self.client.get('http://expul:8000/api/v1/getPost/1')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))

    def test_signup_exp_api(self):
        response = self.client.post('http://expul:8000/api/v1/signup_exp_api/',
                                    {'email': 'a@a.com',
                                     'password': 'password',
                                     'name': 'Mark',
                                     'year': '1994',
                                     'gender': True,
                                     })
        self.assertEqual(response.status_code, 200)


    def test_search_exp_api(self):
        response = self.client.get('http://expul:8000/api/v1/search/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
                'http://expul:8000/api/v1/search/',
                {'searchText': 'Mark'}
        )
        self.assertEqual(response.status_code, 200)