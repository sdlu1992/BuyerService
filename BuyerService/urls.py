from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'main.views.info'),
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
                       url(r'^getOrderListWeb/', 'main.views.get_report'),
                       url(r'^deliver', 'main.views.deliver_goods'),
                       url(r'^refundDecide', 'main.views.refund_decide'),
                       url(r'^addWishList/', 'main.views.add_wish_list'),
                       url(r'^getWishList/', 'main.views.get_wish_list'),
                       url(r'^order/', 'main.views.add_order'),
                       url(r'^getOrder/', 'main.views.get_order'),
                       url(r'^getBuyHistory/', 'main.views.get_buy_history'),
                       url(r'^payForGoods/', 'main.views.pay_for_goods'),
                       url(r'^takeGoods/', 'main.views.take_goods'),
                       url(r'^appraise/', 'main.views.appraise'),
                       url(r'^getAppraiseList/', 'main.views.get_appraise_list'),
                       url(r'^applyRefund/', 'main.views.apply_refund'),
                       url(r'^recharge/', 'main.views.recharge'),
                       url(r'^collect/', 'main.views.add_collection'),
                       url(r'^getCollectList/', 'main.views.get_collection_list'),
                       url(r'^getHome/', 'main.views.get_home'),
                       url(r'^getGoodsBySearch/', 'main.views.get_goods_by_search'),
                       url(r'^getAddressList/', 'main.views.get_address_list'),
                       url(r'^addAddress/', 'main.views.add_address'),
                       url(r'^upload/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': './upload/', 'show_indexes': True}),
                       url(r'^test/', 'main.views.test'),
                       )
