from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from finder.models import Product, SavedProduct
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
import json

def register(response):
    # function for the user registration
    if response.method == 'POST':
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/login/")
        else:
            return redirect("register")
    else:
        form = UserCreationForm()

    return render(response, 'register/register.html', {'form': form})


def account(request):
    # redirects to the user saved products
    user_id = request.user
    sub_list = SavedProduct.objects.filter(username=user_id)
    paginator = Paginator(sub_list, 5)
    page_range = paginator.page_range
    page_number = request.GET.get('page')
    saved_list = paginator.get_page(page_number)    
    context = {
        'paginate': True,
        'saved_list': saved_list,
        'page_range': page_range,
        'page_number': page_number,
    }
    if request.method=='POST':
        sub_list = SavedProduct.objects.filter(username=user_id)
        paginator = Paginator(sub_list, 5)
        page_number = request.POST.get('page')
        saved_list = paginator.get_page(page_number)         
        context = {
            'paginate': True,
            'saved_list': saved_list,
        }              
        return render(request, 'account/nav.html', context)              
    return render(request, 'account/account.html', context)

def delete(request):
    data = {'success': False} 
    if request.method=='POST':
        product = request.POST.get('product')
        SavedProduct.objects.filter(pk=product).delete()    
        data['success'] = True
    return JsonResponse(data)

def nav(request):        
    return render (request, 'account/nav.html')