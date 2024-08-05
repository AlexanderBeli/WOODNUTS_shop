import stripe
from cart.cart import Cart
from django.conf import settings
from django.db import transaction
from django.forms.models import model_to_dict
from django.shortcuts import redirect, render
from django.utils import translation
from django.views import View
from django.views.generic import TemplateView

from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created

# connect to stripe checkout
stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    def post(self, request, pk, *args, **kwargs):
        order_id = pk
        price = Order.objects.get(id=order_id).get_total_cost()
        # order = Order.objects.get(id=order.id)
        # order_id = self.order.id

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": 1,
                        "product_data": {
                            "name": "order " + f"{order_id}",
                            "description": "order",
                        },
                    },
                    "quantity": 1,
                    "price": price,
                    "type": "one_time",
                }
            ],
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        return redirect(checkout_session.url, code=303)


class SuccessView(TemplateView):
    template_name = "paymentsuccess.html"


class CancelView(TemplateView):
    template_name = "paymentcancel.html"


# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["item"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            # запуск оплаты stripe
            price = cart.get_total_price()
            # payment = CreateStripeCheckoutSessionView(
            #     order.id,
            #     price,
            # )
            # checkout_session = stripe.checkout.Session.create(
            #     payment_method_types=["card"],
            #     line_items=[
            #         {
            #             "order_id": order.id,
            #             "price": price,
            #             "currency": "rub",
            #             "type": "one_time",
            #         }
            #     ],
            #     mode="payment",
            #     success_url=settings.PAYMENT_SUCCESS_URL,
            #     cancel_url=settings.PAYMENT_CANCEL_URL,
            # )
            # очистка корзины
            cart.clear()
            # запуск асинхронной задачи
            # transaction.on_commit(lambda: order_created.delay(order.id))
            # order_created.delay_on_commit(order.id)
            # transaction.on_commit(order.pk)
            order_created.delay(order.id)

            return render(request, "order_created.html", {"order": order})
    else:
        form = OrderCreateForm

        current_url = request.path_info
        lang_code = translation.get_language_from_path(current_url)

        if lang_code == "zh-hans":
            lang_code = "zh_hans"
        cat_lang_res = "category_name_" + lang_code
        item_lang_res = "item_name_" + lang_code
        item_desc_lang_res = "item_description_" + lang_code

        for it in cart:
            x = it["item"]
            # for p in x:
            xx = model_to_dict(x)
            it["name"] = xx[item_lang_res]

        return render(request, "order_create.html", {"cart": cart, "form": form})
