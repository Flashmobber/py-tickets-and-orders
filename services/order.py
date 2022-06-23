from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Ticket, Order


def create_order(tickets: list[dict], username: str, date: datetime = None):
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(movie_session_id=ticket["movie_session"],
                                  order=order,
                                  row=ticket["row"],
                                  seat=ticket["seat"])
    return order


def get_orders(username: str = None):
    orders_queryset = Order.objects.all()

    if username:
        orders_queryset = orders_queryset.filter(user__username=username)

    return orders_queryset