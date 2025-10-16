from django import forms
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import User, UserManager, BooksModel, CategoryModel
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError



base_attrs = {'class': 'form-control clrtxt'}

CHOICES = [
    ("Искусство", "Больше об изобразительном искусстве"),
    ("Искусство", "Кино. Телевидение"),
    ("Искусство", "Музыка"),
    ("Искусство", "Архитектура"),
    ("Искусство", "История искусств. Искусствоведение"),
    ("Искусство", "Больше о театре, кино и ТВ"),
    ("Искусство", "История изобразительного искусства"),
    ("Искусство", "Музеи мира. Альбомы репродукций"),
    ("Искусство", "Театр"),
    ("Искусство", "Интерьер. Дизайн. Оформительское искусство"),
    ("Комиксы", ""),
    ("Филология", "Литературоведение. Фольклористика"),
    ("Художественная литература", "Биографии. Мемуары"),
    ("Художественная литература", "Современная проза"),
    ("Манга", ""),
    ("Филология", "Прочие издания по филологии"),
    ("Филология", "Русский язык"),
    ("Филология", "Английский язык"),
    ("Филология", "Другие языки"),
    ("Филология", "Немецкий язык"),
    ("Медицина и здоровье", "Популярная медицина"),
    ("Медицина и здоровье", "Популярные системы сохранения здоровья. Здоровое питание"),
    ("Медицина и здоровье", "Общие вопросы медицины"),
    ("Медицина и здоровье", "Коррекция фигуры. Диеты"),
    ("Детские книги", "Медицина для родителей"),
    ("Медицина и здоровье", "Фитнес. Аэробика"),
    ("Медицина и здоровье", "Атласы анатомии. Медико-биологические дисциплины"),
    ("Медицина и здоровье", "Клиническая медицина в целом"),
    ("Медицина и здоровье", "Специализированные отрасли медицины"),
    ("Медицина и здоровье", "Йога. Пилатес"),
    ("Психология", "Психология отношений. Семья и брак"),
    ("Детские книги", "Психология воспитания и обучения детей"),
    ("Бумажная продукция для офиса", "Календари, ежедневники, планинги"),
    ("Психология", "Психотерапия. Психодиагностика"),
    ("Психология", "Глубинная психология. Психоанализ"),
    ("Художественная литература", "Любовные романы"),
    ("Психология", "Любовь. Эротика. Секс"),
    ("Эзотерика", "Другие эзотерические учения"),
    ("Психология", "Общие вопросы психологии"),
    ("Эзотерика", "Пророки. Предсказания"),
    ("Психология", "Общая теория социальной психологии"),
    ("Искусство", "Живопись и графика. Техники и приемы"),
    ("Наука. Техника. IT", "Информатика"),
    ("Наука. Техника. IT", "Биологические науки"),
    ("Наука. Техника. IT", "Общенаучное знание и теории"),
    ("Наука. Техника. IT", "Технические науки"),
    ("Наука. Техника. IT", "Физико-математические науки"),
    ("История. Общество", "Всемирная история"),
    ("Наука. Техника. IT", "Химия. Научные издания"),
    ("Детские книги", "Детская художественная литература"),
    ("Дом и хобби", "Путешествия и туризм"),
    ("Религия и философия", "Философия"),
    ("Художественная литература", "Публицистика"),
    ("Психология", "Психология успеха. Личная эффективность, мотивация"),
    ("Психология", "Психология общения. Межличностные коммуникации"),
    ("Экономика. Менеджмент. Маркетинг", "Личная эффективность. Мотивация"),
    ("Психология", "Психология личности. Характер, темперамент, талант"),
    ("Экономика. Менеджмент. Маркетинг", "Маркетинг. Реклама"),
    ("Экономика. Менеджмент. Маркетинг", "Экономика. Экономическая теория"),
    ("Экономика. Менеджмент. Маркетинг", "Финансы. Бухгалтерский учет. Аудит"),
    ("Экономика. Менеджмент. Маркетинг", "Бизнес. Предпринимательство. Торговля"),
    ("История. Общество", "Российская история"),
    ("История. Общество", "Политика. Социология. Культура"),
    ("История. Общество", "Военное дело. Спецслужбы"),
    ("Фантастика. Фэнтези", "Мистика. Ужасы"),
]


class CreateBooksForm(forms.Form):

    choices_age_rest = ((1, 'Нет'),
                        (2, '6+'),
                        (3, '12+'),
                        (4, '16+'),
                        (5, '18+'))


    title = forms.CharField(label=_('Название'), max_length=50,
                            widget=forms.TextInput(attrs=base_attrs))
    author = forms.CharField(label=_('Автор'), max_length=20,
                            widget=forms.TextInput(attrs=base_attrs))

    price = forms.IntegerField(label=_('Цена'),
                            widget=forms.TextInput(attrs=base_attrs))
    info_txt = forms.CharField(label=_('Описание'), max_length=1000,
                            widget=forms.TextInput(attrs=base_attrs))
    interpreter = forms.CharField(label=_('Переводчик'),
                            widget=forms.TextInput(attrs=base_attrs))

    publishing_house = forms.CharField(label=_('Издательство'),
                            widget=forms.TextInput(attrs=base_attrs))
    publishing_brand = forms.CharField(label=_('Издательский бренд'),
                            widget=forms.TextInput(attrs=base_attrs))
    series = forms.CharField(label=_('Серия'),
                            widget=forms.TextInput(attrs=base_attrs))  # Серия
    ISBN = forms.CharField(label='ISBN',
                            widget=forms.TextInput(attrs=base_attrs))
    num_page = forms.IntegerField(label=_('Количество страниц'),
                            widget=forms.TextInput(attrs=base_attrs))  # количество страниц
    size = forms.CharField(label=_('Размер'),
                            widget=forms.TextInput(attrs=base_attrs))  # размер
    cover_type = forms.CharField(label=_('Тип обложки'),
                            widget=forms.TextInput(base_attrs))  # Тип обложки
    circulation = forms.IntegerField(label=_('Тираж'),
                            widget=forms.TextInput(attrs=base_attrs))  # тираж
    weight = forms.IntegerField(label=_('Вес'),
                            widget=forms.TextInput(attrs=base_attrs))  # вес
    age_rest = forms.ChoiceField(label=_('Возрастные ограничения'), choices = choices_age_rest,
                            widget=forms.Select(attrs={'class': 'form-select', 'style':'width:10vw'}))  # возрастные ограничения

    img_local = forms.ImageField(label=_('Обложка'),required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'file','id':'img_local'}))


    cat = forms.ChoiceField(label="Категория", choices= CHOICES,
                            widget=forms.Select(attrs={'class': 'form-select', 'style':'width:25vw'}))




class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", min_length=3, max_length=20,
                                 widget=forms.TextInput(attrs=base_attrs))
    last_name = forms.CharField(label="Фамилия", min_length=3, max_length=15,
                                widget=forms.TextInput(attrs=base_attrs))
    phone_number = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs=base_attrs))
    email = forms.EmailField(label=' Почта', widget=forms.TextInput(attrs=base_attrs), max_length=100)
    password1 = forms.CharField(label='Пароль', max_length=100, min_length=5,
                                widget=forms.TextInput(attrs=base_attrs))
    password2 = forms.CharField(label='Подтвердите пароль', max_length=100, min_length=5,
                                widget=forms.TextInput(attrs=base_attrs))
    data_entry = forms.BooleanField(required=True, label='Согласие на обработку данных', widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = User  # Указываю какую модель использовать
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(label='Почта',
                                widget=forms.TextInput(attrs={"autofocus": True, 'class': 'form-control'}))
    password = forms.CharField(label='Пароль', max_length=100, min_length=5,
                               widget=forms.TextInput(attrs=base_attrs),
                               )
