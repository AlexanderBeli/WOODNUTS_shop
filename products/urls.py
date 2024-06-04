from django.urls import path

from .views import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryUpdateView,
    CategoryView,
    ItemCreateView,
    ItemDeleteView,
    ItemDetailView,
    ItemUpdateView,
    ItemView,
    ManagingPageView,
)

urlpatterns = [
    path('', ManagingPageView.as_view(), name='administrating'),
    path('category/list/', CategoryView.as_view(), name='category_all'),
    path('category/add/', CategoryCreateView.as_view(), name='addcategory'),
    path('category/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('item/add/', ItemCreateView.as_view(), name='additem'),
    path('item/list/', ItemView.as_view(), name='item_all'),
    path('item/<int:pk>/edit/', ItemUpdateView.as_view(), name='item_edit'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item_delete'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
]