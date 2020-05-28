from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from finder.models import Product, SavedProduct
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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


def account(request, user_id):
    # redirects to the user saved products
    sub_list = SavedProduct.objects.filter(username=user_id)
    paginator = Paginator(sub_list, 5)
    page_number = request.GET.get('page')
    saved_list = paginator.get_page(page_number) 

    context = {
        'paginate': True,
        'saved_list': saved_list,
    }
    return render(request, 'account/account.html', context)
