"""mumbai61 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
#deprecated next line
# from django.conf.urls import url
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('zerowaste.urls')),
    path('map/',include('map.urls')),
    # path('map/',include('map.urls')),
    # path('i18n/', include('django.conf.urls.i18n')),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    # deprecated
    # url(r'^report_builder/', include('report_builder.urls'))
    re_path(r'^report_builder/', include('report_builder.urls')),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('pages/', include(wagtail_urls)),
]
