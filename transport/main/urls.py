from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('tables_data', views.tables_data),
    path('xml_handler', views.xml_handler)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
