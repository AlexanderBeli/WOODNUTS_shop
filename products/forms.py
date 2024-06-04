from django.forms import ModelForm

from .models import Category, Item


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('item_name_en','item_name_ru','item_name_zh_hans','item_id','item_category_number',
                  'item_picture','item_description_en','item_description_ru','item_description_zh_hans',
                  'item_extra_tag','item_price','item_price_extra_new','item_price_currency')


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('category_number','category_name_ru','category_name_en','category_name_zh_hans')