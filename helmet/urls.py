from django.urls import path
from . import views

urlpatterns = [
      path('',views.base,name='base'),
    path('login',views.login,name='login'),
    path('auth',views.auth,name='auth'),
    path('helmet/', views.helmet, name='helmet'),
    path('accident', views.accident, name='accident'),
    path('crash/',views.crash,name='crash'),#accident
    path('process_video/', views.process_video, name='process_video'),#helmet
    path('rec',views.rec,name='rec')
]