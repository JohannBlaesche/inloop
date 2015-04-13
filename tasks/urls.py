from django.conf.urls import patterns, url

from tasks import views

urlpatterns = patterns(
    '',
    url(
        r'^$',
        views.index,
        name='index'
    ),
    url(
        r'^new_exercise/$',
        views.submit_new_exercise,
        name='new_exercise'
    ),
    url(
        r'^new_category/$',
        views.new_category,
        name='new_category'
    ),
    url(
        r'^(?P<short_id>[\w]+)/edit_category/$',
        views.edit_category,
        name='edit_category'
    ),
    url(
        r'^manage_categories/$',
        views.manage_categories,
        name='man_cat'
    ),
    url(
        r'^category/(?P<short_id>[\w]+)/$',
        views.category,
        name='category'
    ),
    url(
        r'^(?P<slug>[-\w]+)/$',
        views.detail,
        name='detail'
    ),
    url(
        r'^(?P<slug>[-\w]+)/edit/$',
        views.edit,
        name='edit'
    ),
    url(
        r'^(?P<slug>[-\w]+)/results/$',
        views.results,
        name='results'
    ),
    url(
        r'^(?P<slug>[-\w]+)/delete/$',
        views.delete,
        name='delete'
    ),
)
