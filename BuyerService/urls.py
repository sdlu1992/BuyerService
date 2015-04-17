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
    url(r'^changeToSolder/', 'main.views.change_to_solder'),
    url(r'^newGoods/', 'main.views.new_goods'),
    url(r'^report/', 'main.views.report'),
    url(r'^category/', 'main.views.category'),
    url(r'^getGoodsByCategory/', 'main.views.get_goods_by_category'),
    url(r'^good/', 'main.views.get_good'),
    url(r'^addWishList/', 'main.views.add_wish_list'),
    url(r'^getWishList/', 'main.views.get_wish_list'),
    url(r'^order/', 'main.views.add_order'),
    url(r'^test/', 'main.views.test'),
)
