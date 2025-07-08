from django.contrib import admin
from django.urls import path, include
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('core_auth.urls', namespace='core_auth')),
    path('', include(tf_urls)),

]
