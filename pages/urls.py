from django.urls import path

from products.views import (
    ItemDetailViewForClients,
    all_products_view_for_clients,
    category_itemslist_for_clients,
    category_view_for_clients,
    home_view_for_clients,
)

from .views import (
    AboutPageView,
    ClientsPageView,
    ContactUsPageView,
    DeliveryPageView,
    FAQPageView,
    PaymentsPageView,
    PolicyPageView,
)

urlpatterns = [
    path('', home_view_for_clients, name='home'),
    path('popularitems/', category_view_for_clients, name='categorylist'),
    path('allproducts/', all_products_view_for_clients, name='all_products_for_clients'),
    path('<int:pk>/', ItemDetailViewForClients.as_view(), name='item_detail_for_clients'),
    path('category/<int:pk>/', category_itemslist_for_clients, name='category_l'),
    path('contact/', ContactUsPageView.as_view(), name='contactus'),
    path('delivery/', DeliveryPageView.as_view(), name='delivery'),
    path('payments/', PaymentsPageView.as_view(), name='payments'),
    path('policy/', PolicyPageView.as_view(), name='policy'),
    path('clients/', ClientsPageView.as_view(), name='clients'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('faq/', FAQPageView.as_view(), name='faq'),
]