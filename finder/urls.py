from django.urls import path, re_path
from . import views

app_name = 'finder'
urlpatterns = [
    re_path(r'^search/$', views.search, name='search'),
    path('search_auto', views.search_auto, name='search_auto'),
    path('<int:product_id>/', views.detail, name='detail'),
    path('substitute/<int:product_id>/', views.substitute, name='substitute'),    
    path('add/', views.add, name='add'),
    path('sear/', views.search, name='sear') 
]
