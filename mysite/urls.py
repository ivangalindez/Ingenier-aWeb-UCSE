from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login,logout_then_login

from . import views

urlpatterns = [
	url(r'^$', views.post_portada, name='post_portada'),
	url(r'', include('blog.urls')),
	url(r'^post/portada/', views.post_portada, name ='post_portada'),
	#url(r'^post/portada(?P<activacion_token>)/', views.post_confirmar, name ='post_portada'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', views.post_login, name ='post_login' ),
    url(r'^post/logout/$', logout_then_login, name ='post_logout' ),
]