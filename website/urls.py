from django.conf.urls import url
from . import views

app_name = 'website'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<post_id>[0-9]+)', views.post_detail, name='post-detail'),
    url(r'^post/$', views.create_post, name='post-create'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^register/$', views.register_user, name='register')
]