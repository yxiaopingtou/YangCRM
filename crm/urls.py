"""YangCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from crm import views

urlpatterns = [
    url('^$', views.index,name='home'),
    url('^stu_enrollment/$', views.stu_enrollment,name='stu_enrollment'),
    url('^stu_enrollment/approved/(\d+)$', views.enrollment_approved,name='enrollment_approved'),
    url('^enrollment/(\d+)/$', views.enrollment,name='enrollment'),

    url('^enrollment_file-upload/(\d+)/$', views.enrollment_file_upload,name='enrollment_file-upload'),

]
