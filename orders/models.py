from django.db import models
from django.utils.translation import gettext_lazy as _

from products.models import Item


# Create your models here.
class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name=_('first name'))
    last_name = models.CharField(max_length=50, verbose_name=_('last name'))
    email = models.EmailField(verbose_name=_('email'))
    address = models.CharField(max_length=250, verbose_name=_('address'))
    postal_code = models.CharField(max_length=20, verbose_name=_('postal code'))
    city = models.CharField(max_length=100, verbose_name=_('city'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('updated'))
    paid = models.BooleanField(default=False, verbose_name=_('paid'))
    
    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        ordering = ("-created",)
        
    def __str__(self):
        return  _('Order') + ' {}'.format(self.id)
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('order'))
    product = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='order_items', verbose_name=_('item'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('price'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('quantity'))
    
    class Meta:
        verbose_name = _("order item")
        verbose_name_plural = _("order items")
    
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity