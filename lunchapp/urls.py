from django.conf.urls import patterns, url

from lunchapp import views

urlpatterns = patterns('',
	# e.g. /lunchapp/ or /lunchapp/home
    url(r'^$', views.home, name='home'),
	url(r'home', views.home, name='home'),
    # e.g. /lunchapp/2014/1
	url(r'^(?P<year>201[4-9])/(?P<month>[1-9]|1[1-2])/$', views.sign_up, name='sign_up'),
	# e.g. /lunchapp/2014/January
	url(r'(?i)^(?P<year>201[4-9])/(?P<month>January|February|March|April|May|June|July|August|September|October|November|December)/$', views.sign_up, name='sign_up'),
	url(r'(?i)^(?P<year>201[4-9])/(?P<month>January|February|March|April|May|June|July|August|September|October|November|December)/update_lists/$', views.update_lists, name='update_lists'),
)
