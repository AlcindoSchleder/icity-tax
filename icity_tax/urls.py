"""icity_tax URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views
from taxes.api.viewsets import TaxesViewSet

router = routers.DefaultRouter()
router.register(r'taxes', TaxesViewSet, base_name='Taxes') # base_bane é o nome do Modelo da tabela do banco de dados

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/', include(router.urls))
]
