from __future__ import unicode_literals
import uuid
from pytils.translit import slugify
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from googletrans import Translator, constants
from datetime import timedelta
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет пользователя с введенным им email и паролем.
        """
        if not email:
            raise ValueError('Вы не указали почту!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is False:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CategoryModel(models.Model):

    subcategory1 = models.CharField(max_length=100, blank=True)
    subcategory2 = models.CharField(max_length=100, blank=True)

    sub_slugify1 = models.CharField(blank=True, max_length=500)
    sub_slugify2 = models.CharField(blank=True, max_length=500)


    class Meta:
        app_label = 'main'


    def __str__(self):
        return f'({self.subcategory1}) ({self.subcategory2})'

    def save(self, *args, **kwargs):
        self.sub_slugify1 = slugify(self.subcategory1)
        self.sub_slugify2 = slugify(self.subcategory2)
        super(CategoryModel, self).save(*args, **kwargs)


class ReviewsModel(models.Model):
    user_name = models.ForeignKey('User', on_delete=models.PROTECT, related_name='review_user')
    score = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    comment = models.CharField(max_length=200)
    book = models.ForeignKey('BooksModel', null=True, blank=True, related_name='review', on_delete=models.CASCADE)

    pluses = models.CharField(max_length=200, blank=True)
    minuses = models.CharField(max_length=200, blank=True)


class BooksModel(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(blank=True, max_length=100)
    img = models.CharField(max_length=300, blank=True)

    img_local = models.FileField(upload_to='cover', blank=True)

    price = models.IntegerField()
    info_txt = models.CharField(max_length=4000)
    slug_title = models.CharField(blank=True, max_length=500)

    category = models.ManyToManyField(CategoryModel)

    interpreter = models.CharField(blank=True, max_length=100)
    id_book = models.IntegerField(null=True, blank=True, db_index=True)
    publishing_house = models.CharField(blank=True, max_length=100)
    publishing_brand = models.CharField(blank=True, max_length=100)
    series = models.CharField(max_length=100, blank=True)
    year_of_publishing = models.IntegerField(blank=True, null=True)
    ISBN = models.CharField(max_length=100, blank=True)
    num_page = models.IntegerField(blank=True)
    size = models.CharField(max_length=100)
    cover_type = models.CharField(max_length=100)
    circulation = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True)

    publishing = models.BooleanField(default=False)

    age_rest = models.CharField(choices=(('1', 'Нет'), ('2', '6+'), ('3', '12+'), ('4', '16+'), ('5', '18+') ), default='1', blank=True)
    # age_rest = models.IntegerField(blank=True, null=True)

    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name="creator_book")

    def save(self, *args, **kwargs):
        self.slug_title = slugify(self.title)

        # self.title_en = наш перевод
        super(BooksModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.title



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('name'), max_length=30, blank=True)
    last_name = models.CharField(_('surname'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('registered'), auto_now_add=True)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField('is_staff', default=True)  # admin login
    is_superuser = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=12, default='77777777777')

    seller = models.BooleanField(default=True)

    is_verified = models.BooleanField('verified', default=False)
    verification_uuid = models.UUIDField('Unique Verification UUID',    default=uuid.uuid4,
    unique=True,
    editable=False)

    bookmarks = models.ManyToManyField(BooksModel, blank=True, related_name='bookmarks', )
    basket = models.ManyToManyField(BooksModel, blank=True, related_name='basket')
    objects = UserManager()

    products = models.ForeignKey(BooksModel,null=True, blank=True, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):

        return self.first_name



class ViewedModel(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_viewed')
    book = models.ForeignKey('BooksModel', on_delete=models.CASCADE,related_name='book_viewed', blank=True, null=True)
    date_viewed = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_viewed']

    def save(self, *args, **kwargs):
        super(ViewedModel, self).save(*args, **kwargs)

