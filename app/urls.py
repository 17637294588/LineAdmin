"""Online_education URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,re_path
from app import views
from django.views.generic import TemplateView

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'change_cate/(?P<cid>\d+)/',views.Change_cate.as_view()),
    path('get_cate_mes/',views.Get_cate_mes.as_view()),
    path('get_course_mes/',views.Get_course_mes.as_view()),
    re_path(r'get_course_detail/(?P<id>\d+)/',views.Get_course_detail.as_view()),
    re_path(r'chack_type/(?P<id>\d+)/',views.Chack_type.as_view()),
    path('upload_file/',views.Upload_file.as_view()),
    path('upload_img/',views.Upload_img.as_view()),
    path('socket_test',TemplateView.as_view(template_name='socket.html')),
    # path('test_socket',views.test_socket),
    path('socket_push',TemplateView.as_view(template_name='socket_push.html')),
    # path('test_websocket',views.test_websocket),
    path('terminals',views.terminals),
    path('demo',views.demo),
    path('test',views.test),
    path('call_back/',views.Call_back.as_view()),
    path('',views.Youment.as_view()),
    


 
    

]
