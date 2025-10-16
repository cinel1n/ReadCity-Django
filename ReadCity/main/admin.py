from django.contrib import admin
from .models import *
from django.db.models import QuerySet
from .models import *

# from guardian.admin import *
#
#
# class PostAdmin(GuardedModelAdmin):
#     list_display = ["title", ]


#
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from modeltranslation.admin import TranslationAdmin

from modeltranslation.admin import TabbedTranslationAdmin


class BooksTranslationAdmin(TabbedTranslationAdmin):
    pass

# admin.site.register(BooksModel, BooksTranslationAdmin)



class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['id']


class BooksAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'id_book']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['subcategory1', 'subcategory2']

class ViewedAdmin(admin.ModelAdmin):
    list_display = ['date_viewed']

class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'phone_number']

admin.site.register(BooksModel, BooksAdmin)

admin.site.register(CategoryModel, CategoryAdmin)
admin.site.register(ReviewsModel, ReviewsAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(ViewedModel, ViewedAdmin)
