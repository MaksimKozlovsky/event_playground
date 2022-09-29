from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Event, Ticket


@receiver(post_save, sender=Event)
def create_tickets(sender, instance: Event, **kwargs):
    tickets = []

    if kwargs["created"]:
        tickets_amount = instance.ticket_count
        last_number = 0
    else:
        event_tickets = Ticket.objects.filter(event=instance)
        tickets_amount = instance.ticket_count - event_tickets.count()

        if not tickets_amount:
            return

        last_number = event_tickets.last().number

    vip_places = int(tickets_amount * settings.VIP_TICKET_RATE)

    for ticket_num in range(1, tickets_amount - vip_places + 1):
        tickets.append(Ticket(event=instance, price=100, number=ticket_num + last_number))

    for ticket_num in range(1, vip_places + 1):
        tickets.append(Ticket(event=instance, price=200, number=ticket_num + tickets_amount + last_number, vip=True))

    Ticket.objects.bulk_create(tickets)

