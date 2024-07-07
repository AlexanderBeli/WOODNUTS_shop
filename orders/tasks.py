from celery import shared_task
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from .models import Order


@shared_task()
def order_created(order_id):
    """
    Задача для отправки уведомления по электронной поче при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = _('Order') + ' {}'.format(order_id)
    message = _('Dear ') + order.first_name + ",\n\n" + _("You have successfully placed an order.") + "\n" + _("Your order id is ") + str(order_id)
    mail_sent = send_mail(subject, 
                          message,
                          'admin@woodnuts.com',
                          [order.email])
    return mail_sent

