"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
# from .views import *
from . import views

urlpatterns = [
    path("", views.function_api, name="index"),
    path("admin/", admin.site.urls),
   # path("datVisuali/list/<str:statusStaff>/<str:userId>", views.function_api, name="listAppeal")
    path("api/data/list", views.function_api, name="list_ppeal"),
    # path("api/data/predict", views.predict_image, name="list_ppeal")
    path("api/predict/<str:image_url>/", views.predict_image, name="predict_image"),
    path("api/upload/", views.upload_image, name="upload_image")


]

if settings.DEBUG:
    # setting this to view media files from admin panel
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
