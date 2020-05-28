from django.test import TestCase, Client
from django.urls import reverse
from .models import Product, SavedProduct
from django.contrib.auth.models import User
from .views import search


class UrlsTestCase(TestCase):     
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_mentions_page(self):
        response = self.client.get(reverse('mentions'))
        self.assertEqual(response.status_code, 200)


class TestModels(TestCase):
    def setUp(self):

        self.client = Client()
        self.prod = Product.objects.create(
            name=['gazpacho'],
            brand=['alvalle'],
            nutrition_grade='a',
            picture='https://static.openfoodfacts.org/images/products/541/018/803/1072/front_fr.30.400.jpg',
            off_id=5410188031072,
            categories=['aliments et boissons à base de végétaux', " aliments d'origine végétale", ' aliments à base de fruits et de légumes', ' plats préparés', ' soupes', ' réfrigérés', ' soupes de légumes', ' soupes froides', ' plats préparés réfrigérés', ' gaspacho', ' soupes réfrigérées'],
            fat=2.6,
            satured_fat=0.4,
            sugars=3.1,
            salt=0.66,
            real_name='Gazpacho',
            real_brand='Alvalle',
        )

        self.prod_2 = Product.objects.create(
            name=['belvita'],
            brand=['belvita', 'lu', 'mondelez'],
            nutrition_grade='c',
            picture='https://static.openfoodfacts.org/images/products/762/221/044/4141/front_fr.81.400.jpg',
            off_id=7622210444141,
            categories=['snacks', ' snacks sucrés', ' biscuits et gâteaux', ' biscuits', ' biscuits au chocolat'],
            fat=15,
            satured_fat=3.6,
            sugars=21.0,
            salt=0.6,
            real_name='belvita',
            real_brand='Belvita',
        )

        self.prod_3 = Product.objects.create(
            name=['gazpacho','sol'],
            brand=['espanol'],
            nutrition_grade='a',
            picture='https://static.openfoodfacts.org/images/products/541/018/803/1072/front_fr.30.400.jpg',
            off_id=5410188031073,
            categories=['aliments et boissons à base de végétaux', " aliments d'origine végétale", ' aliments à base de fruits et de légumes', ' plats préparés', ' soupes', ' réfrigérés', ' soupes de légumes', ' soupes froides', ' plats préparés réfrigérés', ' gaspacho', ' soupes réfrigérées'],
            fat=2.6,
            satured_fat=0.4,
            sugars=3.1,
            salt=0.66,
            real_name='Gazpacho Sol',
            real_brand='Alvalle Espanol',
        )

        self.user = User.objects.create_user(
            username='Ultraman',
            email='ultraman@gmail.com',
            password='ultraman64'
        )

        self.fav = SavedProduct.objects.create(
            username=self.user,
            sub_product=self.prod,
            original_product=self.prod_2,
        )

        self.query = {'query': 'Du NutellA'}

    def test_Product(self):
        # test if product is saved in Product db
        self.assertEquals(self.prod.name, ['gazpacho'])
        self.assertEquals(self.prod.brand, ['alvalle'])
        self.assertEquals(self.prod.nutrition_grade, 'a')
        self.assertEquals(self.prod.picture, 'https://static.openfoodfacts.org/images/products/541/018/803/1072/front_fr.30.400.jpg')
        self.assertEquals(self.prod.off_id, 5410188031072)    
        self.assertEquals(self.prod.categories, ['aliments et boissons à base de végétaux', " aliments d'origine végétale", ' aliments à base de fruits et de légumes', ' plats préparés', ' soupes', ' réfrigérés', ' soupes de légumes', ' soupes froides', ' plats préparés réfrigérés', ' gaspacho', ' soupes réfrigérées'])
        self.assertEquals(self.prod.fat, 2.6)
        self.assertEquals(self.prod.satured_fat, 0.4)
        self.assertEquals(self.prod.sugars, 3.1)
        self.assertEquals(self.prod.salt, 0.66)
        self.assertEquals(self.prod.real_name, 'Gazpacho')
        self.assertEquals(self.prod.real_brand, 'Alvalle')

    def test_SavedProduct(self):
        # test if product can be saved in a SavedProduct db
        self.assertEquals(self.fav.username, self.user)
        self.assertEquals(self.fav.sub_product, self.prod)
        self.assertEquals(self.fav.original_product, self.prod_2)

    def test_Details(self):
        # test if product has details page
        url = reverse('finder:detail', args=[self.prod_3.id])
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 200)

    def test_Substitute(self):
        # test if product has substitute page
        url = reverse('finder:substitute', args=[self.prod_3.id])
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 200)


class TestSearch(TestCase):
    # check user queries
    def test_Search(self):
        # check with unformatted query
        url = reverse('finder:search')
        url_with_param = "{}?{}".format(url, 'query=GAzpacho')
        self.response = self.client.post(url_with_param)
        self.assertEqual(self.response.status_code, 200)

    def test_EmptySearch(self):
        # test for empty query
        url = reverse('finder:search')
        url_with_param = "{}?{}".format(url, 'query=')
        self.response = self.client.post(url_with_param)
        self.assertEqual(self.response.status_code, 200)

    def test_BogusSearch(self):
        # test for bogus query
        url = reverse('finder:search')
        url_with_param = "{}?{}".format(url, 'query=dzdsfsdfgsvs')
        self.response = self.client.post(url_with_param)
        self.assertEqual(self.response.status_code, 200)
