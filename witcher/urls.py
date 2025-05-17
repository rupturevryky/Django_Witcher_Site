from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'witcher'

urlpatterns = [
    path('', views.witcher_profile, name='profile'),
    path('alchemy/', views.alchemy_items, name='alchemy'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('kaermorhen/', views.kaermorhen, name='kaermorhen'),
    path('gorthur_gvaed/', views.gorthur_gvaed, name='gorthur_gvaed'),
    path('erlenwald/', views.erlenwald, name='erlenwald'),
    path('contracts/', views.contracts, name='contracts'),
    path('contracts/report/', views.generate_report, name='generate_report'),
    path('stats/', views.witcher_stats, name='stats'),
]
