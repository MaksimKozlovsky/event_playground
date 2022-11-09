from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RegisterUserForm

from .models import Event, Ticket, Company, CustomUser
from rest_framework import viewsets, generics, status
from .serializers import EventSerializer, TicketSerializer, CompanySerializer, CustomUserSerializer, UserSerializer


# Create your views here.


# def get_all_events(request):
#     events = Event.objects.all()
#     return JsonResponse({
#         "code": 200,
#         "data": [
#             {
#                 "id": e.id,
#                 "title": e.title,
#                 "count": e.ticket_count,
#                 "organizer_id": e.organizer_id,
#             } for e in events]
#     })


def get_event(request, pk:int):
    event = Event.objects.get(id=pk)
    return JsonResponse({'title': event.title,
                         'count': event.ticket_count})


# @api_view(['GET', 'POST'])
# @csrf_exempt
# def EventViewSet(request):
#     if request.method == 'GET':
#         event = Event.objects.all()
#         serializer = EventSerializer(event, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#
#         serializer = EventSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors)



class SignUpView(CreateView):
    template_name = 'register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register')


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


class CompanySetView(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]


class TicketSetView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]


class EventSetView(generics.RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
def statuss(request):
    return Response({'status': 'OK'}, status=status.HTTP_200_OK)

# Дальше, добавить возможность получать всех юзеров и редактировать выбранного юзера


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    @action(detail=False, methods=['GET'])
    def get_tiers(self, request):
        data = {human_readable: tier for (tier, human_readable) in CustomUser.TIERS}
        return Response(data, status.HTTP_200_OK)


@api_view(['GET'])
def get_one_user(request, pk: int):
    one_user = CustomUser.objects.get(pk=pk)
    serializer = CustomUserSerializer(one_user)
    return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet): # используем только его
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = LimitOffsetPagination
