from django.urls import include, path
from rest_framework import routers
from .views import get_event, \
    get_all_events, \
    SignUpView, \
    EventViewSet, \
    del_event, \
    get_ticket, \
    get_one_ticket, \
    ticket_view_set, CompanySetView, TicketSetView, EventSetView
from . import views

router = routers.DefaultRouter()
# router.register(r'event', views.EventViewSet)
# router.register(r'ticket', views.TicketViewSet)
# router.register(r'company', views.CompanyViewSet)
# отключил чтоб работали другие urls


urlpatterns = [
    path('event/', get_all_events),
    path('event/<int:pk>', get_event),
    path('del_event/<int:pk>', del_event),
    path('register/', SignUpView.as_view(), name='register'),
    path('drf/', EventViewSet),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('all_ticket/', get_ticket),
    path('one_ticket/<int:pk>', get_one_ticket),
    path('buy_ticket/<int:pk>', ticket_view_set),
    path('company/<int:pk>', CompanySetView.as_view()),
    path('even/<int:pk>', EventSetView.as_view()),
    path('tick/', TicketSetView.as_view()),


]
