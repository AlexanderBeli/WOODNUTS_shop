from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import resolve, reverse_lazy
from django.utils import translation
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CategoryForm, ItemForm
from .models import Category, Item


# Ниже идут контроллеры для администраторов для управления сайтом
# Добавлен LoginRequiredMixin
# Позже нужно будет разделить пользователей на две категории - 
# администраторы и пользователи
# и соответственно внести эти изменения в контроллеры
class ManagingPageView(LoginRequiredMixin, TemplateView):
    template_name = 'manager.html'


class ItemCreateView(LoginRequiredMixin, CreateView):
    template_name = 'createitem.html'
    form_class = ItemForm
    # success_url = reverse_lazy('item_detail')
    
    def form_valid(self, form):
        form.save(commit=False)
        form.instance.item_author_id = self.request.user
        form.save()
        return super().form_valid(form)

class CategoryCreateView(LoginRequiredMixin, CreateView):
    template_name = 'createcategory.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category_all')
    
    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author_id = self.request.user
        form.save()
        return super().form_valid(form)


class ItemView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'item_all.html'


class CategoryView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category_all.html'
    

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = (
        'item_name_en',
        'item_name_ru',
        'item_name_zh_hans',
        'item_id',
        'item_category_number',
        'item_picture',
        'item_description_en',
        'item_description_ru',
        'item_description_zh_hans',
        'item_extra_tag',
        'item_price',
        'item_price_extra_new',
        'item_price_currency',
    )
    template_name = 'item_edit.html'
    # success_url = reverse_lazy('item_detail')

    
class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = (
        'category_number',
        'category_name_ru',
        'category_name_en',
        'category_name_zh_hans',
    )
    template_name = 'category_edit.html'
    uccess_url = reverse_lazy('category_all')
    

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'item_delete.html'
    success_url = reverse_lazy('item_all')


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('category_all')
    
    
class ItemDetailView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'item_detail.html'
    
    
class ItemDetailViewForClients(DetailView):
    model = Item
    template_name = 'item_detail_client_page.html'

# Ниже идут функции по отображению страниц для клиентов: 
# страница с товарами по категориям,
# @login_required # работает
def category_view_for_clients(request):
    current_url = request.path_info
    lang_code = translation.get_language_from_path(current_url)
    # cur_language = translation.LANGUAGE_SESSION_KEY
    # category = Category.objects.get()
    if lang_code == 'zh-hans':
        lang_code = 'zh_hans'
    cat_lang_res = 'category_name_' + lang_code
    item_lang_res = 'item_name_' + lang_code
    item_desc_lang_res = 'item_description_' + lang_code
    # category = Category.objects.values(cat_lang_res)
    category = Category.objects.raw(f"""SELECT id, {cat_lang_res} AS cat_name, category_number FROM products_category;""")
    s = ''
    for i in category:
        a = Item.objects.raw(f"""SELECT id,
                                        {item_lang_res} AS item_name,
                                        {item_desc_lang_res} AS item_desc,
                                        item_category_number_id,
                                        item_picture,
                                        item_extra_tag,
                                        item_price,
                                        item_price_extra_new,
                                        item_price_currency,
                                        item_published_at 
                                FROM products_item
                                WHERE item_category_number_id={i.id};""")[:4]
        i.category_number = a
    
    return render(request, 'categorylist.html',{'current_url':category})


def category_itemslist_for_clients(request, pk):
    current_url = request.path_info
    lang_code = translation.get_language_from_path(current_url)
    # cur_language = translation.LANGUAGE_SESSION_KEY
    # category = Category.objects.get()
    if lang_code == 'zh-hans':
        lang_code = 'zh_hans'
    cat_lang_res = 'category_name_' + lang_code
    item_lang_res = 'item_name_' + lang_code
    item_desc_lang_res = 'item_description_' + lang_code
    # category = Category.objects.values(cat_lang_res)
    category = Category.objects.raw(f"""SELECT id, {cat_lang_res} AS cat_name, category_number 
                                        FROM products_category
                                        WHERE id={pk};""")
    s = ''
    for i in category:
        a = Item.objects.raw(f"""SELECT id,
                                        {item_lang_res} AS item_name,
                                        {item_desc_lang_res} AS item_desc,
                                        item_category_number_id,
                                        item_picture,
                                        item_extra_tag,
                                        item_price,
                                        item_price_extra_new,
                                        item_price_currency,
                                        item_published_at 
                                FROM products_item
                                WHERE item_category_number_id={pk};""")
        i.category_number = a
    
    return render(request, 'category_itemslist_forclients.html',{'current_url':category})

