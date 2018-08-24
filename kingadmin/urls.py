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

from django.conf.urls import url
from kingadmin import views

urlpatterns = [

    url('^$', views.king_admin),

    url('^(\w+)/(\w+)/$', views.table_obj_list,name='table_obj_list'),
    url('^(\w+)/(\w+)/(\d+)/change/$', views.table_obj_change,name='table_obj_change'),

    url('^(\w+)/(\w+)/add/$', views.table_obj_add,name='table_obj_add'),
    url('^(\w+)/(\w+)/(\d+)/delete/$', views.table_obj_delete,name='table_obj_delete'),

]
