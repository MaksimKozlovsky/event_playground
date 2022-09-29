from django.urls import include, path
from rest_framework import routers
from .views import get_event, get_all_events, test_drf, SignUpView
from . import views

router = routers.DefaultRouter()
router.register(r'titles', views.EventViewSet)


urlpatterns = [
    path('event/', get_all_events),
    path('event/<int:pk>', get_event),
    path('drf/', test_drf),
    path('register/', SignUpView.as_view(), name='register'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
