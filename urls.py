from django.conf.urls import patterns, include, url

# Womoobox URLs
surveypatterns = patterns('',
    url(r'^$',                                  'survey.views.index'),
    url(r'create/$',                            'survey.views.question_creation'),
    url(r'reset/$',                             'survey.views.reset'),
    url(r'logout/$',                            'django.contrib.auth.views.logout',
                                                    {'next_page': '/login/?next=/'}),
    url(r'login/$',                             'django.contrib.auth.views.login',
                                                    {'template_name': 'login.html'}),
    url(r'(?P<token>[a-zA-Z0-9]+)/answer-it/$', 'survey.views.question_answer'),
    url(r'(?P<token>[a-zA-Z0-9]+)/edit/$',      'survey.views.question_edit'),
    url(r'(?P<token>[a-zA-Z0-9]+)/$',           'survey.views.question_view'),
)
