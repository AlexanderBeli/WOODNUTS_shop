from django.forms.models import model_to_dict
from django.shortcuts import render
from django.utils import translation

from cart.cart import Cart

from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created


# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['item'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            # запуск асинхронной задачи
            order_created.delay(order.id)
            
            return render(request, 'order_created.html', {'order': order})
    else:
        form = OrderCreateForm
        
        current_url = request.path_info
        lang_code = translation.get_language_from_path(current_url)

        if lang_code == 'zh-hans':
            lang_code = 'zh_hans'
        cat_lang_res = 'category_name_' + lang_code
        item_lang_res = 'item_name_' + lang_code
        item_desc_lang_res = 'item_description_' + lang_code

        for it in cart:
            x = it['item']
            # for p in x:
            xx = model_to_dict(x)
            it['name'] = xx[item_lang_res]
        
        return render(request, 'order_create.html', {'cart': cart, 'form': form})
