from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BuyerService.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/', 'main.views.register'),
    url(r'^login/', 'main.views.login'),
    url(r'^info/', 'main.views.info'),
    url(r'^category/', 'main.views.category'),
)
