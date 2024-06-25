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
    
    list_display = ['item_id','item_category_number','item_name_en', 'item_name_ru', 'item_name_zh_hans','item_price', 'item_price_extra_new', 'item_price_currency', 'item_author_id']
    list_filter = ['item_category_number','item_author_id','item_extra_tag','item_price']
    search_fields = ['item_name_en', 'item_name_ru', 'item_name_zh_hans','item_description_en', 'item_description_ru', 'item_description_zh_hans','item_extra_tag','item_price']
    date_hierarchy = 'item_published_at'
    ordering = ['item_price', 'item_published_at','item_id']
    
    list_editable = ['item_name_en', 'item_name_ru', 'item_name_zh_hans','item_price', 'item_price_extra_new', 'item_price_currency']
    list_display_links = ['item_id','item_category_number', 'item_author_id']
    
    def preview(self, obj):
        return mark_safe(f'<img src="{obj.item_picture.url}" style="max-height: 200px;">')
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
