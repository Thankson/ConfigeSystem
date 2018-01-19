from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.repository_list, name='gitweb_repository_list'),
    url(r'^(?P<slug>[\w-]+)/$', views.repository_summary, name='gitweb_repository_summary'),

    url(r'^(?P<slug>[\w-]+)/commit/(?P<commit>[\w-]+)/$', views.repository_commit, name='gitweb_repository_commit'),
    url(r'^(?P<slug>[\w-]+)/commit/(?P<commit>[\w-]+)/diff/$', views.repository_commit, {'template_name': 'repository_commit_diff.html'},
        name='gitweb_repository_commit_diff'),

    url(r'^(?P<slug>[\w-]+)/tree/(?P<branch>[\w-]+)/(?P<path>.*)$', views.repository_tree, name='gitweb_repository_tree'),

    url(r'^(?P<slug>[\w-]+)/log/(?P<branch>[\w-]+)/$', views.repository_log, name='gitweb_repository_log'),
    url(r'^(?P<slug>[\w-]+)/log/$', views.repository_log, name='gitweb_repository_log'),
]