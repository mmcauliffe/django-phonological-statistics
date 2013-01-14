from django.conf.urls.defaults import patterns

urlpatterns = patterns('phonostats.views',
    (r'^$','index'),
    (r'^reset/$','reset'),
    (r'^analysis/$','analyze'),
)

