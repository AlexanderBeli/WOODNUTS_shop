from decimal import Decimal

from django.conf import settings

from products.models import Item


class Cart(object):
    
    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def add(self, item, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        item_id = str(item.pk)
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity': 0,
                                  'price': str(item.item_price)}
        if update_quantity:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity
        self.save()   
        
    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True
    
    def remove(self, item):
        """
        Удаление товара из корзины
        """
        item_id = str(item.pk)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()
            
    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из БД.
        """
        item_ids = self.cart.keys()
        # получение объектов item и добавление их в корзину
        items = Item.objects.filter(id__in=item_ids)
        for item in items:
            self.cart[str(item.pk)]['item'] = item
            
        for item2 in self.cart.values():
            item2['price'] = Decimal(item2['price'])
            item2['total_price'] = item2['price'] * item2['quantity']
            yield item2
            
    def __len__(self):
        """
        Подсчет всех товаров в корзине
        """
        return sum(item2['quantity'] for item2 in self.cart.values())
    
    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине
        """
        return sum(Decimal(item2['price']) * item2['quantity'] for item2 in self.cart.values())
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True