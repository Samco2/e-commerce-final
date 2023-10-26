from django.urls import path
from . import views


app_name = 'UserProfile'
urlpatterns = [
     path('signin', views.signin, name = 'signin'),
     path('signup', views.signup, name = 'signup'),
     path('signout', views.signout, name = 'signout'),
     path('changeaddress', views.changeAddress, name = 'changeaddress'),
      path('dashboard/', views.dashboard, name='dashboard'),
]
