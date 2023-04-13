from django.conf.urls import url 
from tutorials import views 
 
urlpatterns = [ 
    url(r'^home_page$', views.home_page),
    url(r'^column_details$', views.column_names),
    url(r'^chatbot_general$', views.chatbot_general_query),
    url(r'^chatbot_specific$', views.chatbot_specific_query),
    url(r'^district_of_state$', views.district_of_state),
    url(r'^prediction$', views.prediction),
    url(r'^user_location$', views.user_location),
    url(r'^api/tutorials/(?P<pk>[0-9]+)$', views.tutorial_detail),
    url(r'^api/tutorials/published$', views.tutorial_list_published)
]
#url(r'^api/tutorials$', views.tutorial_list),