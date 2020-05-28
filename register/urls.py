from django.urls import path, re_path
from . import views

app_name = 'register'
urlpatterns = [
    path('<int:user_id>/', views.account, name='account'),
    ]
