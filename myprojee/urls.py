from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myprojee.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^crawl/', 'searchprojee.views.crawl_web'),
    url(r'^crawlweb/', 'searchprojee.views.crawl_web_template'),
    url(r'^$', 'searchprojee.views.contact'),
    url(r'^data$', 'searchprojee.views.dataoperations'),
    url(r'^tag$', 'searchprojee.views.tagcloudview'),
    url(r'^bootstrap$', 'searchprojee.views.bootstrap'),
    url(r'^stat$', 'searchprojee.views.stattable'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^indexbook$', 'searchprojee.views.indexbk')                   
)
