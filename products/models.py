import boto3
from boto3.session import Session
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from PIL import Image

# from raw_sugar import RawManager

# Create your models here.
# def get_currencies():
#     return {i: i for i in settings.CURRENCIES}

def generate_path_and_image(instance, filename):
    return 'item_pictures/' + str(instance.item_id) + '.' + 'webp'


class Item(models.Model):
    class AdditionalInfo(models.TextChoices):
        FancyProduct = 'Fancy Product', _('Fancy Product') #Новинка
        Sale = 'Sale', _('Sale')                           #Распродажа
        SpecialItem = 'Special Item', _('Special Item')    #Спец предложение
        Bestseller = 'Bestseller', _('Bestseller')         #Хит продаж
        __empty__ = _("Unknown")
        InStock = 'In Stock',_('In Stock')                 #В наличии
        NotInStock = 'Not In Stock',_('Not In Stock')      #Не в наличии
        
    item_id = models.IntegerField(auto_created=True, unique=True, verbose_name=_('item number'))
    item_author_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        auto_created=True,
        on_delete=models.CASCADE,
        verbose_name=_('author')
        )

    # Валидация будет во view. Если ни одно из наименований не будет заполнено, сохранено не будет
    # Валидацию также нужно будет по соответствию яык наименования (ячейка) = языку текста (ячейка) = выбранная валюта
    # При выборе языка будут отражаться только те товары, которые были добавлены на данном языке
    # Соответственно валюта будет автоматически отражаться в зависимости от языка
    # китайский - юань, русский - рубль
    # вопрос к евро и доллару - зависит от направленности торговли, для Европы - евро, Штаты - доллар
    # Если добавить возможность выбора валюты на сайте, тогда это будет только в ознакомительных целях
    # При добавлении в корзину цена будет указана в двух валютах - валюте рассчета, в зависимости от выбранного языка
    # и в "ознакомительной валюте"
    # Что если пользователь выберет один язык, добавит в корзину товар, затем переключит язык 
    # и попытается добавить товар? Разные цены и разные регионы.
    # Нужно будет реализовать невозможность поменять язык или невозможность добавить товар в корзину с другой валютой
    # По окончанию оформления товара вывести сообщение: Ваш заказ получен, в ближайшее время с вами свяжется
    # оператор для уточнения деталей заказа.
    item_name_en = models.CharField(max_length=200, unique=True, blank=True, null=True, verbose_name=_('item name in English'))
    item_name_ru = models.CharField(max_length=200, unique=True, blank=True, null=True, verbose_name=_('item name in Russian'))
    item_name_zh_hans = models.CharField(max_length=200,unique=True, blank=True, null=True, verbose_name=_('item name in Chinese'))
    
    item_category_number = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        verbose_name=_('category')
    )
    # в файле отработчике написать логику конвертирования в формат webp
    # добавить в отработчик переименование файла в соответствие с item_name
    item_picture = ProcessedImageField(verbose_name=_('picture'), upload_to=generate_path_and_image,
                             format='WEBP',
                             options={'quality': 70}) # upload_to="item_pictures"
    
    item_description_en = models.TextField(blank=True, verbose_name=_('item description in English'))
    item_description_ru = models.TextField(blank=True, verbose_name=_('item description in Russian'))
    item_description_zh_hans = models.TextField(blank=True, verbose_name=_('item description in Chinese'))
    
    item_extra_tag = models.CharField(choices=AdditionalInfo, default=AdditionalInfo.__empty__, verbose_name=_('item extra tag'))
    
    item_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('item price'))
    item_price_extra_new = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name=_('extra new item price'))
    item_price_currency = models.CharField(max_length=3, choices=settings.CURRENCY_CHOICES, default='RUB', verbose_name=_('item price currency'))
    
    item_published_at = models.DateField(auto_now_add=True)
    
    # objects = RawManager()
    
    # slug = models.SlugField('Название в виде url', max_length=200)
    
    # def get_absolute_url(self):
    #     return reverse('post_detail', args={'slug': self.slug})
    
    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")
        ordering = ["-item_published_at"]
        
        
    def __str__(self) -> str:
        return str(self.item_id)
        # if self.item_name_en == '':
        #     if self.item_name_ru == '':
        #         if self.item_name_zh_Hans == '':
        #             return ValueError
        #         else:
        #             return self.item_name_zh_Hans
        #     else:
        #         return self.item_name_ru
        # else:
        #     return self.item_name_en
        
        
        # for i in [self.item_name_en, self.item_name_ru, self.item_name_zh_Hans]:
        #     if i != '':
        #         return i

    def get_absolute_url(self):
        # return reverse("item_all")
        return reverse('item_detail', kwargs={'pk': self.pk}) #args=[str(self.pk)])
    
    def delete(self, *args, **kwargs):
        session = Session(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        s3_resource = session.resource('s3')
        s3_bucket = s3_resource.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        
        file_path = 'media/' + str(self.item_picture)
        response = s3_bucket.delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': file_path
                    }
                ]
            })
        # return super(Item, self).delete(*args, **kwargs)
        
        # s3 = boto3.resource('s3')
        # session = Session (settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        # object = s3_resource.Object(settings.AWS_STORAGE_BUCKET_NAME, str(self.item_picture)).delete()
                
        return super(Item, self).delete(*args, **kwargs)


class Category(models.Model):
    category_number = models.IntegerField(auto_created=True, unique=True, verbose_name=_('category number'))
    author_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        auto_created=True,
        on_delete=models.CASCADE,
        verbose_name=_('author')
        )

    category_name_ru = models.CharField(max_length=50, verbose_name=_('category name in Russian'))
    category_name_en = models.CharField(max_length=50, verbose_name=_('category name in English'))
    category_name_zh_hans = models.CharField(max_length=50, verbose_name=_('category name in Chinese'))

    
    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ["category_number"]
        
        
    def __str__(self) -> str:
        # return str(self.category_number)
        return self.category_name_ru
        
    
    def right_language(self):
        language = 'information'
        return language
    
    
    def get_absolute_url(self):
        return reverse("category_all")
    