import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
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

def search_algorithm(query, lang_code):
    
    if lang_code == 'zh-hans':
        lang_code = 'zh_hans'
    cat_lang_res = 'category_name_' + lang_code
    item_lang_res = 'item_name_' + lang_code
    item_desc_lang_res = 'item_description_' + lang_code
    
    query2 = str(query)
    
    object_list = Item.objects.none()
    query2_list = ''
    query3 = ''
    query_basic = f"""SELECT products_item.id,
                                item_id,
                                item_author_id_id,
                                item_published_at,
                                item_name_ru,
                                item_name_en,
                                item_name_zh_hans,
                                item_category_number_id,
                                item_picture,
                                item_extra_tag,
                                item_price,
                                item_price_extra_new,
                                item_price_currency,
                                item_description_ru,
                                item_description_en,
                                item_description_zh_hans,
                                {cat_lang_res} AS cat_name
                        FROM products_item 
                        JOIN products_category 
                        ON products_item.item_category_number_id=products_category.id """
    
    if query2.isdigit():
        query2 = int(query2)
        query = None
        
    elif bool(re.search(r'[0-9]', query2)):
        
        only_numbers_str = re.sub(r'[^0-9|\s]', '', query2) # нужно сохранить пробелы
        only_numbers_str = only_numbers_str.strip()
        
        if only_numbers_str.isdigit():
            
            x = query2
            query2 = int(only_numbers_str)
            query = re.sub(r'[0-9]', '', x)
            
        else:
            x = only_numbers_str.split()
           
            if len(x) > 1:
                query3 = query2
                query2_list = re.findall(r'\d+', query2)
                
                query = re.sub(r'[0-9]', '', query3)
                
                if query.strip() == '':
                    query = ''
            else:
                query3 = query2
                query2 = re.sub(r'[^0-9]', '', query2)
                query = re.sub(r'[0-9]', '', query3)
                if query.strip() == '':
                    query = ''

    else:
        query2 = ''

    if query2_list and isinstance(query, str):
        query_basic += f""" WHERE products_category.{cat_lang_res} iLIKE '%%' || '{query}' || '%%'
                        OR products_item.{item_lang_res} iLIKE '%%' || '{query}' || '%%'
                        OR to_tsvector(coalesce(products_item.{item_lang_res}, '') || ' ' ||
                            coalesce(products_item.{item_desc_lang_res},'')) @@ plainto_tsquery('{query}')
                        OR  similarity(coalesce(products_item.{item_lang_res}, '') || ' ' ||
                            coalesce(products_item.{item_desc_lang_res},''), '{query}') > 0.1 """
        
        for x in query2_list:
            x = int(x)
            query_basic += f""" OR item_id={x}
                    OR item_price={x}
                    OR item_price_extra_new={x}"""
        object_list = Item.objects.raw(query_basic)

    elif query2_list and query == '':
        
                        
        for x in query2_list:
            x = int(x)
            query_basic += f""" WHERE item_id={x}
                    OR item_price={x}
                    OR item_price_extra_new={x}"""
        object_list = Item.objects.raw(query_basic)
        
    elif isinstance(query2, int) and isinstance(query, str):
        query_basic += f""" WHERE products_category.{cat_lang_res} iLIKE '%%' || '{query}' || '%%'
                            OR products_item.{item_lang_res} iLIKE '%%' || '{query}' || '%%'
                            OR to_tsvector(coalesce(products_item.{item_lang_res}, '') || ' ' ||
                                coalesce(products_item.{item_desc_lang_res},'')) @@ plainto_tsquery('{query}')
                            OR  similarity(coalesce(products_item.{item_lang_res}, '') || ' ' ||
                                coalesce(products_item.{item_desc_lang_res},''), '{query}') > 0.1
                            OR item_id={query2}
                            OR item_price={query2}
                            OR item_price_extra_new={query2};"""
        object_list = Item.objects.raw(query_basic)
        
    elif isinstance(query2, int):
        query_basic += f""" WHERE item_id={query2}
                            OR item_price={query2}
                            OR item_price_extra_new={query2} 
                            ORDER BY item_published_at DESC;"""
        object_list = Item.objects.raw(query_basic)
    elif isinstance(query, str):    
        query_basic += f""" WHERE products_category.{cat_lang_res} iLIKE '%%' || '{query}' || '%%'
                            OR products_item.{item_lang_res} iLIKE '%%' || '{query}' || '%%'
                            OR to_tsvector(coalesce(products_item.{item_lang_res}, '') || ' ' ||
                                coalesce(products_item.{item_desc_lang_res},'')) @@ plainto_tsquery('{query}')
                            OR  similarity(coalesce(products_item.{item_lang_res}, '') || ' ' ||
                                coalesce(products_item.{item_desc_lang_res},''), '{query}') > 0.1
                            ORDER BY item_published_at DESC;"""
        object_list = Item.objects.raw(query_basic)
    
    else:
        object_list = Item.objects.all()

    return object_list

class SearchResultsLstViewForClients(ListView):
    model = Item
    template_name = 'search_results.html'
    paginate_by = 8
    
    def get_queryset(self):
        # query = self.request.GET.get('q')
        # return Item.objects.filter(
        #     Q(item_name_ru__icontains=query) | Q(item_name_en__icontains=query)
        # )
        query = self.request.GET.get('q')
        current_url = self.request.path_info
        lang_code = translation.get_language_from_path(current_url)
        
        return search_algorithm(query, lang_code)


class ItemView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'item_all.html'
    paginate_by = 8
    
    def get_queryset(self):
        query = self.request.GET.get('q')

        current_url = self.request.path_info
        lang_code = translation.get_language_from_path(current_url)
        
        return search_algorithm(query, lang_code)

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
    # uccess_url = reverse_lazy('category_all')
    

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
    category = Category.objects.raw(f"""SELECT id, {cat_lang_res} AS cat_name
                                        FROM products_category
                                        WHERE id={pk};""")
    # s = set()
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
        # i.category_number = a
        # s.add(a)
    paginator = Paginator(a, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'category_itemslist_forclients.html',{'current_url':category, 'page_obj': page_obj})


def all_products_view_for_clients(request):
    current_url = request.path_info
    lang_code = translation.get_language_from_path(current_url)

    if lang_code == 'zh-hans':
        lang_code = 'zh_hans'
    cat_lang_res = 'category_name_' + lang_code
    item_lang_res = 'item_name_' + lang_code
    item_desc_lang_res = 'item_description_' + lang_code

    a = Item.objects.raw(f"""SELECT id,
                                    {item_lang_res} AS item_name,
                                    {item_desc_lang_res} AS item_desc,
                                    item_picture,
                                    item_extra_tag,
                                    item_price,
                                    item_price_extra_new,
                                    item_price_currency,
                                    item_published_at 
                            FROM products_item;""")
 
    paginator = Paginator(a, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'all_products_view_for_clients.html',{'page_obj': page_obj})


def home_view_for_clients(request):
    current_url = request.path_info
    lang_code = translation.get_language_from_path(current_url)

    if lang_code == 'zh-hans':
        lang_code = 'zh_hans'
    cat_lang_res = 'category_name_' + lang_code
    item_lang_res = 'item_name_' + lang_code
    item_desc_lang_res = 'item_description_' + lang_code

    a = Item.objects.raw(f"""SELECT id,
                                    {item_lang_res} AS item_name,
                                    {item_desc_lang_res} AS item_desc,
                                    item_picture,
                                    item_extra_tag,
                                    item_price,
                                    item_price_extra_new,
                                    item_price_currency,
                                    item_published_at 
                            FROM products_item
                            WHERE item_extra_tag IN ('Fancy Product','Special Item','Bestseller','In Stock');""")[:8]
    return render(request, 'home.html',{'page_obj': a})
