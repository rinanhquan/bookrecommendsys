
from django.contrib import admin
from django.urls import path,include
admin.site.site_header = 'My admin'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('core.urls')),
]
