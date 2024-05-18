from django.contrib import admin
from django.urls import path, include
from foodbot import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('foodbot/', include('foodbot.urls')),
    path('callback/', views.callback, name='callback'),
    path('<str:name>/home/', views.home_view, name='home'),
    path('<str:name>/index/', views.index_view, name='index'),
    path('<str:name>/3060/', views.a3060_view, name='a3060'),
    path('<str:name>/90/', views.a90_view, name='a90'),
    path('<str:key>/<str:view_type>/submit/', views.handle_submission, name='handle_submission'),
]