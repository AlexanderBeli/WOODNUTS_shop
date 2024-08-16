from django.urls import path

from .views import (
    CancelView,
    CreateStripeCheckoutSessionView,
    SuccessView,
    order_create,
    order_detail_view,
    order_list,
)

urlpatterns = [
    path("create/", order_create, name="order_create"),
    path(
        "create/<int:pk>/",
        CreateStripeCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path("create/<int:pk>/success/", SuccessView.as_view(), name="success"),
    path("create/<int:pk>/cancel/", CancelView.as_view(), name="cancel"),
    path("list/", order_list, name="orderlists"),
    path("list/order/<int:pk>/", order_detail_view, name="orderdetail"),
]
