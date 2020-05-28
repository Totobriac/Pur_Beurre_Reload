from django.core.management.base import BaseCommand
from finder.models import Product
import requests
import unicodedata
import re


class Command(BaseCommand):
    # create a Django command to populate the database
    help = "populate the database"

    def handle(self, *args, **kwargs):
        self.categories_list()
        self.fill_db()

    def categories_list(self):
    # retrieves from the OpenFoodsFacts API a list of the categories
    # returns a list of categories
        self.categories = []
        self.response = requests.get("https://fr.openfoodfacts.org/categories&json=1")
        self.data = self.response.json()
        i = 0
        for category in self.data["tags"]:
            if category["products"] >= 1200:
                self.name = category["name"]
                self.categories.append(self.name)
                i += 1

        print("It's ok, imported %s" % i)
        return self.categories

    def fill_db(self):
        # populate the database
        # each product has is OpenFoodsFacts id added to a list to avoid to import twice the same product
        self.product_id_list = []
        self.total = 0
        for category in self.categories:
            self.parameters = {
                "action": "process",
                "json": True,
                "page_size": 10,
                "tagtype_0": "categories",
                "tag_contains_0": 'contains',
                'tag_0': category,
                "page": 1
            }

            while self.parameters['page'] <= 30:
                self.response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", self.parameters)
                self.data = self.response.json()

                try:
                    for i in range(len(self.data["products"])):
                        self.off_id = self.data['products'][i]['id']
                        # check if product as already been imported
                        if self.off_id not in self.product_id_list:
                            self.product_id_list.append(self.off_id)
                            try:
                                self.all_datas = []
                                self.brands_list = []
                                self.category_list = []
                                self.real_name = self.data['products'][i]['product_name']                     
                                self.name = self.data['products'][i]['product_name'].lower()
                                self.list_name = re.split("[- ’? ; , ' . : ' ' " " ]", self.name)
                                self.formatted_name = [strip_accents(x) for x in self.list_name]
                                self.brands = self.data['products'][i]['brands_tags']
                                for brand in self.brands:
                                    self.brands_list.append(brand.split('-'))
                                    self.final_brands_list = [x for xs in self.brands_list for x in xs]
                                self.nutriscore = self.data['products'][i]['nutriscore_grade']
                                self.picture = self.data['products'][i]['image_url']                                
                                self.categories = self.data['products'][i]['categories'].lower()
                                self.split_categories = list(self.categories.split(","))
                                self.fat = self.data['products'][i]['nutriments']['fat_value']
                                self.saturated_fat = self.data['products'][i]['nutriments']['saturated-fat_value']
                                self.sugars = self.data['products'][i]['nutriments']['sugars_value']
                                self.salt = self.data['products'][i]['nutriments']['salt']
                                self.real_name = self.data['products'][i]['product_name']
                                self.real_brand_list = (self.data['products'][i]['brands']).split(',')
                                self.real_brand = self.real_brand_list[0]
                                try:                               
                                    if len(self.list_name[0]) == 0 or len(self.brands[0]) == 0 or len(self.nutriscore[0]) == 0 or len(self.picture[0]) == 0 or len(self.categories) == 0:
                                        pass
                                    else:
                                        self.total += 1
                                        self.all_datas.append("%s, %s, %s" % (self.real_name, self.real_brand, self.total))
                                        print(self.all_datas)
                                        p = Product(real_name=self.real_name, name=self.formatted_name, brand=self.final_brands_list, nutrition_grade=self.nutriscore, picture=self.picture, off_id=self.off_id, categories=self.split_categories, fat=self.fat, satured_fat=self.saturated_fat, sugars=self.sugars, salt=self.salt, real_brand=self.real_brand)
                                        p.save()
                                        print('save ok')
                                except IndexError:
                                    pass

                            except KeyError:
                                pass
                        else:
                            pass
                except KeyError:
                    pass
                self.parameters["page"] +=1    


def strip_accents(text):
    # strip the accents of a text
    try:
        text = unicode(text, 'lower_caseutf-8')
    except NameError:
        pass
    text = unicodedata.normalize('NFD', text)\
        .encode('ascii', 'ignore')\
        .decode("utf-8")
    return str(text)
