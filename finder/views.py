from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Product, SavedProduct
from .management.commands.populate_db import strip_accents
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import re
from django.shortcuts import redirect
stopwords = ['le', 'la', 'les', 'en', 'a', 'au', 'aux', 'd', 'des', 'et', 'de']


def index(request):
    # redirect to the main page
    template = loader.get_template('finder/main_page.html')
    return HttpResponse(template.render(request=request))


def mentions(request):
    # redirect to the 'mentions légales' page
    template = loader.get_template('finder/mentions.html')
    return HttpResponse(template.render(request=request))


def search(request):
    # process the input from the user
    # input format : str
    # return a list of str
    query = request.GET.get('query')
    query_lower = query.lower()
    list_name = re.split("[- ’? ; , ' . : ' ' " " ]", query_lower)
    stripped_query = [strip_accents(x) for x in list_name]
    clean_query = [word for word in stripped_query if word not in stopwords]

    #compare the list of str to 'name' & 'brand' of every product in Product
    # if every str of the list matches saves the product in match_list[]
    # returns a list of int
    match_list = []
    for x in Product.objects.all():
        match = 0
        for y in clean_query:
            if y in x.name or y in x.brand:
                match += 1
                if match == len(clean_query):
                    match_list.append(x.id)
            else:
                pass

    if not query:
        products_list = Product.objects.all()
    else:
        products_list = Product.objects.filter(id__in=match_list)

    title = "Choissisez le produit qui correspond à votre demande: "

    # paginate the result
    paginator = Paginator(products_list, 9)
    page = request.GET.get('page', 1)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'title': title,
        'paginate': True,
        'query': query
    }
    # render the result to search.html
    return render(request, 'finder/search.html', context)


def detail(request, product_id):
    # redirect to the details page of a product    
    product = Product.objects.get(pk=product_id)
    return render(request, 'finder/detail.html', {'product': product})


def substitute(request, product_id):
    # find food substitute for the selected product
    product = Product.objects.get(pk=product_id)
    product_categories = eval(product.categories)
    match_list = []

    # compares the starting 4 categories of the product with those of the other products in the database
    # returns a list of matching products in descending order from their 'nutrition-grade'
    for x in Product.objects.all():
        if x.id != product_id:
            match = 0
            for y in product_categories[0:4]:
                print(y)
                if y not in eval(x.categories):
                    break
                elif y in eval(x.categories):
                    match += 1
                    if match == 4:
                        match_list.append(x.id)

    substitute_product = Product.objects.filter(id__in=match_list).order_by('nutrition_grade')

    # paginate the result
    paginator = Paginator(substitute_product, 9)
    page = request.GET.get('page', 1)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'product': product,
    }

    return render(request, 'finder/substitute.html', context)


def save(request, product_id, sub_product_id):
    #  saves the selected product and its substitute into a database
    sub_product = Product.objects.get(pk=sub_product_id)
    original_product = Product.objects.get(pk=product_id)
    user = request.user
    previous_page = request.META['HTTP_REFERER']
    p = SavedProduct(username=user, sub_product=sub_product, original_product=original_product)
    p.save()

    response = redirect(previous_page)
    return response
