from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Category, Item


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name_en','category_number','author_id')
    

class ItemAdmin(admin.ModelAdmin):
    fields = ['item_author_id', 'item_id', 'item_name_en', 'item_name_ru', 'item_name_zh_hans', 'item_category_number',
              'item_picture', 'preview', 'item_description_en', 'item_description_ru', 'item_description_zh_hans',
              'item_extra_tag','item_price', 'item_price_extra_new', 'item_price_currency']
    readonly_fields = ["preview"]
    
    list_display = ('item_name_en', 'item_name_ru', 'item_name_zh_hans', 'item_id','item_category_number','item_author_id')
    
    def preview(self, obj):
        return mark_safe(f'<img src="{obj.item_picture.url}" style="max-height: 200px;">')
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
