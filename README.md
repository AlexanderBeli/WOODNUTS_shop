<h1>Проект Интернет-Магазин</h1>
<h2>Описание:</h2>
<div>
    <p>Интернет магазин "Лесной орех", специализирующийся на продаже орехов, сухофруктов, восточных сладостях и специй.</p>
</div>
<h2>Статистика:</h2>
<div>
<p>Стоит принять во внимание, что во время курсов многое не было объяснено и не было даже упомянуто, например, работа с сессиями, контекстом в джанго и др., следовательно, во время выполнения проекта достаточно много времени уходило на поиск качественного материала, решение различных задач.
</p>
</div>
<h2>Этапы:</h2>
<div>
    <p>05.08.2024 Добавил возможность экспортировать заказы в CSV файлы из админки.</p>
    <p>05.08.2024 Постарался привязать Stripe. Информация отправляется, но выскакивает ошибка You may only specify one of these parameters: price, price_data. Пока не разобрался как это решить.</p>
    <p>03.08.2024 Вернулся после перерыва, перенес БД на новое устройство.</p>
    <p>09.07.2024 Celery, RabbitMQ, Flower решают поставленные задачи</p>
    <p>06.07.2024 Запустил Celery через Docker.</p>
    <p>03.07.2024 Прикрутил Celery.</p>
    <p>01.07.2024 Реализована логика и отражение страницы оформления заказа.</p>
    <p>29.06.2024 Реализовал отражение информации о корзине в шапке сайта (кол-во товара, общая стоимость).</p>
    <p>28.06.2024 Настроил отражение формы добавления товара в корзину, используя внутренние настройки виджетов и внешние настройки bootstrap.</p>
    <p>27.06.2024 Добавлена функция добавления товара в корзину в различных разделах сайта, на странице поиска.</p>
    <p>27.06.2024 Переработана логика отражения имен товаров в корзине при смене языка сайта.</p>
    <p>26.06.2024 Реализована корзина заказа при помощи сессий. Отработана функция добавления и отражения товара в корзине покупателя.</p>
    <p>25.06.2024 Оптимизировал и расширил функциоанл админки: теперь добавлена возможность редактировать информацию нескодьких товаров одновременно.</p>
    <p>24.06.2024 Оптимизировал код алгоритма поиска, поиск работает исправно с разным количеством данных, как с цифрами, так и со словами одновременно. Вопрос с пагинацией. Она разбивает количество по заданному параметру. Единственный момент, что при нажатии на страницу, пагинация сбивается и срабатывает по всем элементам. Как вывод - перебрать пагинацию, на данный момент оставим это за пределами проекта.</p>
    <p>18.06.2024 Улучшил алгоритм поиска, теперь можно делать поиск по цифрам (по цене, ID), используя в том числе regex. (v.2.1)</p>
    <p>14.06.2024 реализовал поиск по категориям, заголовку и описанию, используя Full text Search, Trigram Extension и raw query, так как сайт многоязычный. (v.2.0)</p>
    <p>09.06.2024 реализовал пагинацию, настроил логику отражения товаров на главной странице</p>
    <p>04.06.2024 Удалил по ошибке views.py, восстановил. Оптимизировал БД (перевод сайта на кит язык), добавил пару тегов к товарам. (v.1.9)</p>
    <p>03.06.2024 Реализовал следующий функционал для пользователей: 1) просмотр товара по категориям, 2) просмотр товаров по категории, 3) просмотр отдельной странице товара. Написал логику переводов этих страниц в зависимости от выбранного языка сайта. (v.1.8)</p>
    <p>28.05.2024 Настроил конвертирование картинок при загрузке в формат 'webp' и переименование картинок в формате ID товара + '.webp'. Благодаря этому оптимизируется использование места в хранилище, например 5,3 кб вместо 98,5 кб. (v.1.7)</p>
    <p>24.05.2024 Настроил отправку и сохранение картинок через форму на сайте на Amason S3. Настроил удаление картинок через форму не только в качестве удаления записи в БД, но также и на Amason S3.</p>
    <p>Возник вопрос – если добавляется описание на всех языках, валюту можно добавить только одну. Что будет при отражении? Если поставить взаимосвязь валюты и языка, то по факту будет отражаться только на одном языке. Ограничить языком сайта и поставить валюту по умолчанию? Для каждого языка создавать отдельное объявление с фиксированной валютой? Может тогда лучше создать отдельные таблицы в БД по языкам?
    Категории отражать в цифрах или на англ языке?
    </p>
    <p>На данный момент сайт ориентирован на клиентов в РФ, перевод на иностранные языки сделан с целью ознакомления предложения в России. Следовательно, будет одна валюта доступна по умолчанию – рубли, добавлю возможность видеть перерасчет на другие национальные валюты для справки. Все расчеты будут происходить в рублях. В будущем, при необходимости, подкорректирую эти настройки.</p>
    </p>
    <p>17.05.2024 Добавил формы добавления/изменения/удаления/просмотра на сайт. (v.1.6)</p>
    <p>14.05.2024 Создал мультиязычную модель "Товары" со следующими полями: автор, код товара, наименование товара на английском языке, наименование товара на русском языке, наименование товара на китайском языке, номер категории, картинка, описание товара на английском языке, описание товара на русском языке, описание товара на китайском языке, цена товара, валюта денежной единицы, время добавления товара. Добавил просмотр картинки в админке. (v.1.5)</p>
    <p>13.05.2024 настроил, подключил, протестировал Amazon S3 storage</p>
    <p>06.05.2024 добавил страницы "О нас", "Доставка" и др., содержащие статическую информацию. Усовершенствовал логику сайта, улучшил site map, добавил страницу администрирования сайта. Добавил функционал по изменению/удалению категорий. Улучшил дизайн сайта. (v.1.4)</p>
    <p>04.05.2024 отладил перевод динамических и статических страниц, добавил аутентификацию для доступа к чувствительной информации, настроил добавление категорий через сайт авторизованным пользователям (настроил автоматическое добавление автора в БД при добавлении категории), настроил проверку уникальности номеров категорий при добавлении (v.1.3)</p>
    <p>03.05.2024 Настроил мультиязычную БД категорий и их динамическое отражение на сайте. (v.1.2)</p>
    <p>30.04.2024 Исправил три момента. Может быть убрать кнопку "Найти"? - убрал. Нужно ли заморочиться с отображением поля ввода даты рождения в зависимости от особеннойстей языков?</p>
    <p>26.04.2024 после перерыва вернулся к проекту. Обнаружил три момента, где необходимо подправить: 
    
    1. Вопрос к внешнему виду:
    Есть диапазон, когда еще не появляется кнопка, но и не на всю ширину экрана. В этот момент шапка плывет, не очень красиво --- необходимо подправить.
    
    2. Eще один момент – внесение даты. Нужно подправить, чтобы появлялся календарь и выбор шел только оттуда (было реализовано в GUI Tkinter) и чтобы соответственно было в секундах сохранено в БД. --- необходимо исправить
    
    3. После регистрации автоматически пересылка на страницу, которая красиво не настроена. --- исправить
</p>
    <p>04.04.2024 Настроил автоматическое отражение информации на странице регистрации вместе с выпадающим списком в соответствие с выбранным языком. Настроил переключение логотипа в зависимости от выбранного языка. (v.1.1)</p>
    <p>25.03.2024 Завершил дизайн главной страницы</p>
    <p>23.03.2024 Создал сменяющиеся картинки для карусели</p>
    <p>22.03.2024 Создал логотип компании</p>
    <p>19.03.2024 Создал модель пользователя с необходимыми полями в связи с условиями задачи, в том числе необязательные поля "пол" и "дата рождения", создал формы регистрации, входа и выхода из аккаунта</p>
</div>
<div>
    <p></p>
    <p></p>
</div>