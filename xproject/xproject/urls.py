from django.conf.urls import url, include
from addresses import views
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('addresses/', views.address_list),
    path('addresses/<int:pk>/', views.address),
    path('login/', views.login),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('^$', views.login_page),
    path('app_login/', views.app_login),
    path('app_signup/',views.app_signup),

    #카메라 추가
    path('app_addface/',views.app_app_addface),
    path('app_opendoor/',views.app_app_opendoor),

   
]
 #파일 추가
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)