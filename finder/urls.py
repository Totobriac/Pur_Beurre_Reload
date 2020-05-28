from django.urls import path, re_path
from . import views

app_name = 'finder'
urlpatterns = [
    re_path(r'^search/$', views.search, name='search'),
    path('<int:product_id>/', views.detail, name='detail'),
    path('substitute/<int:product_id>/', views.substitute, name='substitute'),
    path('saved/<int:product_id>/<int:sub_product_id>', views.save, name='save'),
]
