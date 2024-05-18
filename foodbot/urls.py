from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('callback', views.callback)
]
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)