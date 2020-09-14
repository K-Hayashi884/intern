from django import template
from django.urls import reverse
from django.utils.html import format_html

from ..models import Message

register = template.Library()

@register.filter
def msg_id_to_obj(msg_id):
    if msg_id:
        msg = Message.objects.get(id=msg_id)
        return msg
    else:
        return False
