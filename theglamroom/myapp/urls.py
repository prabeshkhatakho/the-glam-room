from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('hairstyle/', views.hairstyle, name='hairstyling'),
    path('makeup/', views.makeup, name='makeups'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('gallery/search/', views.gallery_search, name='gallery_search'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('AboutUsCategory/<int:id>/', views.AboutUsCategory_detail, name='AboutUsCategory_detail'),
    path('contact/<int:artist_id>/', views.contact_artist, name='contact_artist'),
    

   

]
