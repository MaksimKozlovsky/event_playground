from django.urls import include, path
from rest_framework import routers
from .views import get_event, \
    SignUpView, \
    EventViewSet, \
    del_event, \
    get_ticket, \
    get_one_ticket, \
    ticket_view_set, CompanySetView, TicketSetView, EventSetView, statuss, CustomUserViewSet, get_one_user
    # modify_tier  ,get_all_events


from . import views

router = routers.DefaultRouter()
router.register(r'all_events', EventViewSet)
#router.register(r'ticket', views.TicketViewSet)
router.register(r'company', views.CompanyViewSet)
router.register(r'users', CustomUserViewSet)


urlpatterns = [
#    path('event/', get_all_events),
    path('status/', statuss),
    path('event/<int:pk>', get_event),
    path('del_event/<int:pk>', del_event),
    path('register/', SignUpView.as_view(), name='register'),
#    path('drf/', EventViewSet),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('all_ticket/', get_ticket),
    path('one_ticket/<int:pk>', get_one_ticket),
    path('buy_ticket/<int:pk>', ticket_view_set),
    path('company/<int:pk>', CompanySetView.as_view()),
    path('even/<int:pk>', EventSetView.as_view()),
    path('tick/', TicketSetView.as_view()),
    path('ping/', statuss),
    path('one_user/<int:pk>', get_one_user),


]
