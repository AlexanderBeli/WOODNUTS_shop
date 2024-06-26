from django.shortcuts import get_object_or_404, redirect, render
from django.utils import translation
from django.views.decorators.http import require_POST

from products.models import Item

from .cart import Cart
from .forms import CartAddProductForm


# Create your views here.
@require_POST
def cart_add(request, pk):
    cart = Cart(request)
    item = get_object_or_404(Item, id=pk)
    
    current_url = request.path_info
    lang_code = translation.get_language_from_path(current_url)

    if lang_code == 'zh-hans':
        lang_code = 'zh_hans'
    cat_lang_res = 'category_name_' + lang_code
    item_lang_res = 'item_name_' + lang_code
    item_desc_lang_res = 'item_description_' + lang_code

    cart_product_form = CartAddProductForm()
    
    # item = Item.objects.raw(f"""SELECT pk,
    #                                 {item_lang_res} AS item_name,
    #                                 {item_desc_lang_res} AS item_desc,
    #                                 item_picture,
    #                                 item_extra_tag,
    #                                 item_price,
    #                                 item_price_extra_new,
    #                                 item_price_currency,
    #                                 item_published_at 
    #                         FROM products_item
    #                         WHERE pk={pk};""")

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            item=item,
            quantity=cd['quantity'],
            update_quantity=cd['update']
        )
    return redirect('cart_detail')

def cart_remove(request, pk):
    cart = Cart(request)
    item = get_object_or_404(Item, id=pk)
    cart.remove(item)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})