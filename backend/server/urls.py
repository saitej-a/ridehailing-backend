"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from auth_user.urls import urlpatterns as main_urls
from driver.urls import urlpatterns as driver_urls
from ride.urls import urlpatterns as ride_urls
from rider.urls import urlpatterns as rider_urls  
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(main_urls)),
    path('api/driver/', include(driver_urls)),
    path('api/ride/', include(ride_urls)),
    path('api/rider/', include(rider_urls)),
]
