from django.contrib.auth.models import User, AbstractUser
from django.db import models

# Create your models here.


class BaseDateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser):

    TIERS = (
        ('G', 'gold'),
        ('S', 'silver'),
        ('P', 'platinum')
    )
    tier = models.CharField(max_length=150, choices=TIERS, null=True, blank=True)

    def __str__(self):
        return self.username


class Event(BaseDateMixin):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', null=True)
    date = models.DateField(verbose_name='Дата проведения', null=True)
    organizer = models.ForeignKey(
        'Company',
        verbose_name='Организатор',
        on_delete=models.SET_NULL,
        null=True,
        related_name="event",
    )
    sponsors = models.ManyToManyField(
        'Company',
        verbose_name='Спонсоры',
        related_name="+"
    )
    ticket_count = models.PositiveIntegerField(verbose_name='Количество билетов')

    def __str__(self):
        # TODO кол-во занятных билетов минусовать
        return f'{self.title} | {self.ticket_count}'

    def save(self, *args, **kwargs):
        tickets_amount = Ticket.objects.filter(event=self).count()
        if self.ticket_count < tickets_amount:
            self.ticket_count = tickets_amount
        super().save(*args, **kwargs)


class Ticket(BaseDateMixin):
    event = models.ForeignKey(
        'Event',
        verbose_name='Название мероприятия',
        on_delete=models.CASCADE
    )
    price = models.PositiveIntegerField(verbose_name='Цена')
    number = models.PositiveIntegerField(verbose_name='Номер билета')
    vip = models.BooleanField(verbose_name='Статус билета "ВИП"', default=False)
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Посетитель',
        on_delete=models.CASCADE, null=True,
    )

    def __str__(self):
        return f'{self.event} | {self.user}'

    class Meta:
        verbose_name = 'Ticket'


class Company(BaseDateMixin):
    title = models.CharField(max_length=100, verbose_name='Наименование организации')


