from django.conf.urls import url
from . import views

namespace = 'website'

urlpatterns = [
    url(r'^', views.index, name='index'),
]