from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'sshbox.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'app.views.home_view', name = 'home'),
    url(r'^list/$', 'app.views.list_view', name = 'list'), 
    url(r'^launch/$', 'app.views.launch_view', name = 'launch'),
    url(r'^admin/', include(admin.site.urls)),
]