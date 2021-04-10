from django.urls import path,include
from imageapp import views
from django.conf.urls import url


urlpatterns = [
    path('',views.Home, name = 'home'),
    path('upload-image/',views.UploadImage, name = 'upload-image'),

    path('signup', views.SignupView, name='signup-view'),
    path('auth', views.AuthView, name='auth-view'),

    path('login', views.LoginView, name='login'),
    path('logout', views.LogoutView, name='login-out'),    

    path('edit/<int:pk>/', views.EditImage, name='edit-image'),
    path('rotate-anti/<int:pk>/', views.RotateAnti, name='rotate-anti'),
    path('rotate-clock/<int:pk>/', views.RotateClock, name='rotate-anti'),
    
    path("<single_slug>", views.TagCategory, name='single_slug'),
]
