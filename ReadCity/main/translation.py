from modeltranslation.translator import translator, TranslationOptions
from main.models import BooksModel
from main.forms import CreateBooksForm


class BooksTranslationOptions(TranslationOptions):
    fields = ('title', 'author', 'info_txt', 'interpreter', 'publishing_house', 'publishing_brand', 'series', 'cover_type')

class CreateBooksOptions(TranslationOptions):
    fields = ('title', 'author', 'info_txt', 'interpreter', 'publishing_house', 'publishing_brand', 'series', 'cover_type')

translator.register(BooksModel, BooksTranslationOptions)