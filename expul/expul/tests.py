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

    #ensures the request works and that there are 3 categories
    def test_getallcatname(self):
        response = self.client.get('http://expul:8000/api/v1/getallcatname/')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        num_cats = len(deser)
        self.assertEqual(num_cats, 3)

    #makes sure create post request works
    #also ensures it is in the correct cateogry and subcategory
    def test_create_listing_exp_api(self):
        response = self.client.get('http://expul:8000/api/v1/postbycat/1')
        self.assertEqual(response.status_code, 200)
        deser1 = json.loads(response.content.decode("utf-8"))
        numPostsCat = len(deser1)
        response = self.client.get('http://expul:8000/api/v1/postbysubcat/2')
        self.assertEqual(response.status_code, 200)
        deser2 = json.loads(response.content.decode("utf-8"))
        numPostsSubCat = len(deser2)

        url = 'http://expul:8000/api/v1/create_listing_exp_api/'
        #auth 123 is used a a dummy authentication in the db to simplify testing
        response = self.client.post(url,
                                    {'category': '1',
                                     'subcategory': '2',
                                     'title': 'Creating',
                                     'summary': 'Test Posting',
                                     'price': '1.23',
                                     'auth': 123,
                                     })
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
                'http://expul:8000/api/v1/search/',
                {'searchText': 'Creating'}
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get('http://expul:8000/api/v1/postbycat/1')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        newnumPostsCat = len(deser)
        self.assertEqual(newnumPostsCat, numPostsCat+1)

        response = self.client.get('http://expul:8000/api/v1/postbysubcat/2')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        newnumPostsSubCat = len(deser)
        self.assertEqual(newnumPostsSubCat, numPostsSubCat+1)

    def test_create_post_wrong_cat(self):
        url = 'http://expul:8000/api/v1/create_listing_exp_api/'
        response = self.client.post(url,
                                    {'category': '21',
                                     'subcategory': '2',
                                     'title': 'Creating',
                                     'summary': 'Test Posting',
                                     'price': '1.23',
                                     'auth': 123,
                                     })
        deser = json.loads(response.content.decode("utf-8"))
        self.assertEqual(deser, {})

    def test_create_post_wrong_sub_cat(self):
        url = 'http://expul:8000/api/v1/create_listing_exp_api/'
        response = self.client.post(url,
                                    {'category': '1',
                                     'subcategory': '72',
                                     'title': 'Creating',
                                     'summary': 'Test Posting',
                                     'price': '1.23',
                                     'auth': 123,
                                     })
        deser = json.loads(response.content.decode("utf-8"))
        self.assertEqual(deser, {})

    def test_get_posts_by_category(self):
        response = self.client.get('http://expul:8000/api/v1/getallcatname/')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        num_cats = len(deser)
        for i in range (1, num_cats):
            response = self.client.get('http://expul:8000/api/v1/postbycat/'+ str(i))
            self.assertEqual(response.status_code, 200)
        #test one that does not exist
        response = self.client.get('http://expul:8000/api/v1/postbycat/17')
        self.assertEqual(response.status_code, 200)

    def test_get_posts_by_subcategory(self):
        response = self.client.get('http://expul:8000/api/v1/postbysubcat/1')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('http://expul:8000/api/v1/postbysubcat/2')
        self.assertEqual(response.status_code, 200)

    def test_getcatname(self):
        response = self.client.get('http://expul:8000/api/v1/getcatname/1')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        self.assertEqual(deser['catName'], 'Bikes')

        response = self.client.get('http://expul:8000/api/v1/getcatname/2')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        self.assertEqual(deser['catName'], 'Books')

        response = self.client.get('http://expul:8000/api/v1/getcatname/3')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        self.assertEqual(deser['catName'], 'Toys')

        response = self.client.get('http://expul:8000/api/v1/getcatname/7')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        self.assertEqual(deser, {})

    def test_getSubcatName(self):
        response = self.client.get('http://expul:8000/api/v1/getsubcatname/1')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        self.assertEqual(deser['subcatName'], 'Mystery')

        response = self.client.get('http://expul:8000/api/v1/getsubcatname/2')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        self.assertEqual(deser['subcatName'], 'Mountain')

        response = self.client.get('http://expul:8000/api/v1/getsubcatname/11')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        self.assertEqual(deser, {})

    def test_getAllSubCatName(self):
        response = self.client.get('http://expul:8000/api/v1/getallsubcatname/')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        #it returns a dict of the categories and subcategories
        self.assertEqual(deser['1']['2'], 'Mountain')

    def test_getCatNameFromSubcat(self):
        #testing one that does exist
        response = self.client.get('http://expul:8000/api/v1/catname/1')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        self.assertEqual(deser['categoryName'], 'Books')

        #tests one that does not exist
        response = self.client.get('http://expul:8000/api/v1/catname/7')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        self.assertEqual(deser, {})

    def test_login_exp_api(self):
        response = self.client.get('http://expul:8000/api/v1/login_exp_api/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            'http://expul:8000/api/v1/login_exp_api/',
            {'email': 'mdh3hc@virginia.edu', 'password': 'hello' }
        )
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        self.assertEqual(deser, {})

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
        self.assertEqual(deser['error'], 'post not found')

        response = self.client.get('http://expul:8000/api/v1/getPost/135')
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        self.assertEqual(deser['title'], 'For Testing')

    def test_signup_exp_api(self):
        response = self.client.post('http://expul:8000/api/v1/signup_exp_api/',
                                    {'email': 'a@a.com',
                                     'password': 'password',
                                     'name': 'Mark',
                                     'year': '1994',
                                     'gender': 1,
                                     })
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        if deser['ok']:
            self.assertEqual(deser['resp']['user_id'], 22)
        else:
            #You need to dumpdata in models again
            self.assertEqual(deser['ok'], False)


    def test_search_exp_api(self):
        response = self.client.get('http://expul:8000/api/v1/search/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
                'http://expul:8000/api/v1/search/',
                {'searchText': 'Mark'}
        )
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        self.assertEqual(deser, [])
        
        response = self.client.post(
                'http://expul:8000/api/v1/search/',
                {'searchText': 'Creating'}
        )
        self.assertEqual(response.status_code, 200)
        deser = json.loads(response.content.decode("utf-8"))
        self.assertEqual(deser[0]['title'], 'Creating')