from django.urls import path, re_path
from . import views

app_name = 'register'
urlpatterns = [
    path('account/', views.account, name='account'),
    path('account/nav/', views.nav, name='nav'),
    path('delete/', views.delete, name='delete'),
]
