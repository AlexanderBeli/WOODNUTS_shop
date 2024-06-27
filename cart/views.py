from django.forms.models import model_to_dict
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
    
    cart_product_form = CartAddProductForm()

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
        
         
    return render(request, 'cart_detail.html', {'cart': cart})