from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RegisterUserForm

from .models import Event, Ticket, Company
from rest_framework import viewsets
from .serializers import EventSerializer, TicketSerializer, CompanySerializer
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


@api_view(['GET', 'POST'])
@csrf_exempt
def EventViewSet(request):
    if request.method == 'GET':
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)



class SignUpView(CreateView):
    template_name = 'register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register')


# class EventViewSet(viewsets.ModelViewSet):
#     queryset = Event.objects.all().order_by('title')
#     serializer_class = EventSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().order_by('number')
    serializer_class = TicketSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('title')
    serializer_class = CompanySerializer

# as_view
# class EventViewSet(APIView):
#     def get(self, request):
#         lst = Event.objects.all().values()
#         return Response({'event': list(lst)})
#
#     def post(self, request):
#         # event_new = Event.objects.created(
#         #     title=request.data['title'],
#         #     description=request.data['description']
#         # )
#         return Response({'event': 'lnfkbzb kdfbib'})


@api_view(['DELETE'])
def del_event(request, pk: int):
    try:
        idd = Event.objects.get(pk=pk)
        idd.delete()
    except:
        print('Не существует')
    return Response(status=204)


@api_view(['GET'])   # URL buy_ticket
@permission_classes([IsAdminUser])
def get_ticket(request):
    all_ticket = Ticket.objects.all()
    serializer = TicketSerializer(all_ticket, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_one_ticket(request, pk: int):
    one_ticket = Ticket.objects.get(pk=pk)
    serializer = TicketSerializer(one_ticket)
    return Response(serializer.data)


@api_view(["GET", "POST"])   # URL buy_ticket
@permission_classes([IsAuthenticated])   # если билет купили -> dell
def ticket_view_set(request, pk: int):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "GET":
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)
    elif request.method == "POST":              # Доделать пример с покупко билета на пользователя при POST запросе
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            ticket.user = request.user
            ticket.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)

