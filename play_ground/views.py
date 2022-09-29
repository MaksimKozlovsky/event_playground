from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework.decorators import api_view
from .forms import RegisterUserForm

from .models import Event
from rest_framework import viewsets
from .serializers import EventSerializer
# Create your views here.


def get_all_events(request):
    events = Event.objects.all()
    return JsonResponse({
        "code": 200,
        "data": [
            {
                "id": e.id,
                "title": e.title,
                "count": e.ticket_count,
                "organizer_id": e.organizer_id,
            } for e in events]
    })


def get_event(request, pk:int):
    event = Event.objects.get(id=pk)
    return JsonResponse({'title': event.title,
                         'count': event.ticket_count})


@api_view()
def test_drf(request):
    pass


class SignUpView(CreateView):
    template_name = 'register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register')


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('title')
    serializer_class = EventSerializer
