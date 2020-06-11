from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Product, SavedProduct
from .management.commands.populate_db import strip_accents
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import re
from django.shortcuts import redirect
stopwords = ['le', 'la', 'les', 'en', 'a', 'au', 'aux', 'd', 'des', 'et', 'de']
from django.http import JsonResponse
import json


def index(request):
    # redirect to the main page
    template = loader.get_template('finder/main_page.html')
    return HttpResponse(template.render(request=request))


def mentions(request):
    # redirect to the 'mentions légales' page
    template = loader.get_template('finder/mentions.html')
    return HttpResponse(template.render(request=request))

def search(request):
    if request.method=='GET':     
        query = request.GET.get('query')    
        query_lower = query.lower()
        list_name = re.split("[- ’? ; , ' . : ' ' " " ]", query_lower)
        stripped_query = [strip_accents(x) for x in list_name]
        clean_query = [word for word in stripped_query if word not in stopwords]    
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
        paginator = Paginator(products_list, 9)
        page = request.GET.get('page', 1)
        page_range = paginator.page_range    
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
            'query': query,
            'page_range': page_range,
        }        
        return render(request, 'finder/search.html', context)

    if request.method=='POST':        
        answer = request.POST.get('query')
        splitted = answer.split(' ')
        print(splitted)
        query_list = splitted[0:-1]
        query = ' '.join(query_list)                
        query_lower = query.lower()
        list_name = re.split("[- ’? ; , ' . : ' ' " " ]", query_lower)
        stripped_query = [strip_accents(x) for x in list_name]
        clean_query = [word for word in stripped_query if word not in stopwords]          
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
        paginator = Paginator(products_list, 9)
        page = splitted[-1]        
        page_range = paginator.page_range    
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
            'query': query,
            'page_range': page_range,
        }                     
        return render(request, 'finder/sear.html', context)

def detail(request, product_id):
    # redirect to the details page of a product    
    product = Product.objects.get(pk=product_id)
    return render(request, 'finder/detail.html', {'product': product})


# def substitute(request, product_id):
def substitute(request, product_id):
    # find food substitute for the selected product
    if request.method=='GET':               
        product = Product.objects.get(pk=product_id)
        product_categories = eval(product.categories)
        match_list = []
    
        for x in Product.objects.all():
            if x.id != product_id:
                match = 0
                for y in product_categories[0:4]:                    
                    if y not in eval(x.categories):
                        break
                    elif y in eval(x.categories):
                        match += 1
                        if match == 4:
                            match_list.append(x.id)

        substitute_product = Product.objects.filter(id__in=match_list).order_by('nutrition_grade')

        paginator = Paginator(substitute_product, 9)
        page_range = paginator.page_range
        print(page_range)
        page = request.GET.get('page')        
        try:
            products = paginator.page(page)
        except PageNotAnInteger:            
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        
        context = {
            'products': products,
            'product': product,
            'paginate': True,
            'page_range': page_range,
        }

        return render(request, 'finder/substitute.html', context)

def sub (request):
    if request.method=='POST':
        answer = request.POST.get('query')
        splitted = answer.split(' ')
        product_id = splitted[0]
        page = splitted[1]
        product = Product.objects.get(pk=product_id)
        product_categories = eval(product.categories)
        match_list = []
    
        for x in Product.objects.all():
            if x.id != product_id:
                match = 0
                for y in product_categories[0:4]:                    
                    if y not in eval(x.categories):
                        break
                    elif y in eval(x.categories):
                        match += 1
                        if match == 4:
                            match_list.append(x.id)

        substitute_product = Product.objects.filter(id__in=match_list).order_by('nutrition_grade')

        paginator = Paginator(substitute_product, 9)
        page_range = paginator.page_range
        
              
        try:
            products = paginator.page(page)
        except PageNotAnInteger:            
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        
        context = {
            'products': products,
            'product': product,
            'paginate': True,
            'page_range': page_range,
        }
        return render(request, 'finder/sub.html', context)







def add(request):
    data = {'success': False} 
    if request.method=='POST':
        product = request.POST.get('product')
        user = request.user       
        splitted = product.split(' ')
        sub_product = Product.objects.get(pk=(splitted[1]))
        original_product = Product.objects.get(pk=(splitted[0]))       
        p = SavedProduct(username= user, sub_product=sub_product, original_product = original_product)
        p.save()        
        data['success'] = True
    return JsonResponse(data)
    
def search_auto(request):
  if request.is_ajax():    
    q = request.GET.get('term', '')
    products = Product.objects.filter(real_name__icontains=q)    
    results = []
    for pr in products:
        product_json = {'value':0, 'img':0, 'label':0}
        product_json['value'] = pr.real_name
        product_json['label'] = pr.real_name
        product_json['img'] = pr.picture               
        results.append(product_json)            
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)
