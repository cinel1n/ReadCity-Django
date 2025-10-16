from typing import Any

from django.http import HttpResponse
from django.template.loader import render_to_string

from django.shortcuts import render
from django.views.generic import FormView, ListView
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.http import Http404
from django.core.cache import cache
from datetime import date
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView, View
from rest_framework.generics import UpdateAPIView, ListAPIView, \
    DestroyAPIView, RetrieveAPIView, CreateAPIView
# from django.utils.translation import gettext as _
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.decorators import action
from .forms import LoginUserForm, CreateUserForm, CreateBooksForm
from .add_scripts import validation
from django.shortcuts import redirect
from django.views.generic.base import ContextMixin
from .serializers import *
from rest_framework.response import Response

def delete_cache_keys():
    try:
        categories = CategoryModel.objects.all()
    except Exception:
        categories = []

    cache.delete('new_books_home')
    cache.delete('all_books')

    for cat in categories:
        cache.delete(f'cat_filter_{cat.subcategory1}')

    directions = ('ascend', 'descend')
    filters = ('title', 'author', 'price')

    for direction in directions:
        for field in filters:
            for cat in categories:
                cache.delete(f'{direction}_{field}_{cat.subcategory1}_sort')



class Context(ContextMixin):

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        sub = {}

        book_category = cache.get_or_set('cached_book_category', CategoryModel.objects.all(), 3600**2)

        for cat in book_category:
            sub[cat.subcategory1] = cat.sub_slugify1

        if not self.request.user.is_anonymous:
            get_user = self.request.user
            context['bookmarks'] = get_user.bookmarks.all()
            context['basket_books'] = get_user.basket.all()

        context['cat'] = sub

        return context


class HomePageView(ListView, Context):
    model = BooksModel

    def get_queryset(self):
        books_all = cache.get_or_set('all_books', self.model.objects.all())

        return cache.get_or_set('new_books_home', books_all.order_by('-id')[:6])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        viewed = ViewedModel.objects.all()

        if not user.is_anonymous:
            get_user = User.objects.get(email=user.email)
            viewed = viewed.filter(user=get_user).select_related('book')
            viewed = [i.book for i in viewed]
            count_viewed = len(viewed)

            context['viewed'] = viewed[:6] if count_viewed >=6 else viewed

        else:
            context['viewed'] = None

        return context


class BookmarksView(ListView, Context):
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_book'] = True
        return context


class BookView(ListView, Context):
    template_name = 'book.html'
    model = BooksModel

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        get_book = cache.get_or_set(f'book_{self.kwargs['id']}',
                                    self.model.objects.get(id_book=self.kwargs['id']))
        get_user = self.request.user

        if not get_user.is_anonymous:
            ViewedModel.objects.create(user=get_user, book=get_book)

        context['book'] = get_book

        property_book1 = {
            "Переводчик": get_book.interpreter,
            "ID": get_book.id_book,
            "Издательство": get_book.publishing_house,
            "Серия": get_book.series,
            "Год публикации": get_book.year_of_publishing,

        }
        property_book2 = {
            'Издательский бренд':get_book.publishing_brand,
            "ISBN": get_book.ISBN,
            "Количество страниц": get_book.num_page,
            "Размер": get_book.size,
            "Тип обложки": get_book.cover_type,
            "Тираж": get_book.circulation,
            "Вес": get_book.weight,
            "Возрастное ограничение": get_book.age_rest,
        }
        context['property_book1'] = property_book1
        context['property_book2'] = [property_book1, property_book2]
        return context

    def get_queryset(self):

        get_book = cache.get_or_set(f'book_{self.kwargs['id']}',
                                    self.model.objects.get(id_book=self.kwargs['id']))
        category = get_book.category.all()[0]

        return cache.get_or_set(f'books_{category.sub_slugify1}',
            BooksModel.objects.filter(category=category))[:6]


class MyProductsView(ListView, Context):
    model = BooksModel
    paginate_by = 18

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return []
        return self.model.objects.filter(creator=self.request.user)



class AuthorizationView(LoginView, Context):
    form_class = LoginUserForm

    def get_success_url(self):
        return reverse('home')



def verify(request, uuid):
    try:
        user = User.objects.get(verification_uuid=uuid, is_verified=False)
    except User.DoesNotExist:
        raise Http404("User does not exist or is already verified")

    user.is_verified = True
    user.save()
    return render(request, 'activate.html')

def logout_(request):
    logout(request)
    return redirect('/')


class LibraryView(ListView, Context):
    model = BooksModel
    template_name = "library.html"
    paginate_by = 18

    def get_queryset(self):
        category = cache.get_or_set('cat_filter_' + self.kwargs['book'], CategoryModel.objects.filter(sub_slugify1=self.kwargs['book']))
        books = cache.get_or_set('all_books', BooksModel.objects.all())

        if len(category) != 0:
            return books.filter(category__in=category)

        return books


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs['book'] != 'all':
            context['category'] = cache.get('cat_filter_'+self.kwargs['book'])[0].subcategory1

        else:
            context['category'] = 'Все книги'

        return context


@require_http_methods(['GET'])
def filter_books(request, cat_sort, filter, direction):
    title_cache = f'{direction}_{filter}_{cat_sort}_sort'

    if direction == "descend":
        filter = '-' + filter

    if cat_sort == "all":

        book_list = cache.get_or_set(title_cache, BooksModel.objects.order_by(filter))

    else:
        book_list = cache.get_or_set(title_cache, BooksModel.objects.filter(category__in=CategoryModel.objects.filter(subcategory1=cat_sort)).order_by(filter))

    return render(request, "library.html", {'object_list':book_list, 'category':cat_sort})


@require_http_methods(['POST'])
def book_marks_delete(request, id):
    print(11)
    book_add = BooksModel.objects.get(id_book=id)
    request.user.bookmarks.remove(book_add)
    return HttpResponse('<div></div>')

@require_http_methods(['POST'])
def book_marks_add(request, id):
    book_add = BooksModel.objects.get(id_book=id)
    request.user.bookmarks.add(book_add)
    return HttpResponse('<div></div>')

@require_http_methods(['POST'])
def delete_all_bookmarks(request):
    request.user.bookmarks.clear()
    return HttpResponse('<h1 style="margin: 40px 0">Книги были удалены</h1>')

@require_http_methods(['POST'])
def basket_delete(request, id):
    book = BooksModel.objects.get(id_book=id)
    user = request.user
    for i in user.basket.filter(id_book=book.id_book):
        user.basket.remove(i)

    return HttpResponse("<div> </div>")

@require_http_methods(['POST'])
def basket_add(request, id):
    book = BooksModel.objects.get(id_book=id)
    request.user.basket.add(book)
    html = render_to_string('includes/basket_buttons.html',  request=request)

    return HttpResponse(html)




class SearchBookView(ListView, Context):
    model = BooksModel
    template_name = "library.html"

    def get_queryset(self):
        s = self.request.GET.get('s', '').strip()
        if not s:
            return self.model.objects.none()

        return self.model.objects.filter(
            Q(title__icontains=s) |
            Q(author__icontains=s) |
            Q(interpreter__icontains=s) |
            Q(series__icontains=s) |
            Q(info_txt__icontains=s) |
            Q(ISBN__icontains=s) |
            Q(category__subcategory1__icontains=s) |
            Q(category__subcategory2__icontains=s)
        ).distinct()

class BasketView(ListView, Context):
    model = BooksModel


class CreateBooksView(FormView, Context):
    form_class = CreateBooksForm
    template_name = 'create_entry.html'
    success_url = reverse_lazy('home')


    def form_valid(self, form):

        model_book = BooksModel()

        model_book.title = form.cleaned_data['title']
        model_book.author =  form.cleaned_data['author']

        try:
            model_book.img_local = self.request.FILES['img_local']

        except:
            form.add_error('img_local', 'Загрузите фотографию')
            return self.form_invalid(form)

        model_book.price =  form.cleaned_data['price']
        model_book.info_txt =  form.cleaned_data['info_txt']

        cat = form.cleaned_data['cat'].split(' / ')

        model_book.interpreter =  form.cleaned_data['interpreter']
        model_book.publishing_house =  form.cleaned_data['publishing_house']
        model_book.publishing_brand =  form.cleaned_data['publishing_brand']

        model_book.id_book = BooksModel.objects.all().reverse()[0].id_book+1
        model_book.series =  form.cleaned_data['series']
        model_book.year_of_publishing = date.today().year
        model_book.ISBN =  form.cleaned_data['ISBN']
        model_book.num_page =  form.cleaned_data['num_page']
        model_book.size =  form.cleaned_data['size']
        model_book.cover_type =  form.cleaned_data['cover_type']
        model_book.circulation =  form.cleaned_data['circulation']
        model_book.weight =  form.cleaned_data['weight']
        model_book.age_rest = form.cleaned_data['age_rest']

        model_book.creator = self.request.user
        model_book.save()

        model_book.category.set(CategoryModel.objects.filter(subcategory1=cat[0], subcategory2=cat[1]))

        model_book.save()

        delete_cache_keys()

        return super().form_valid(form)

class MailView(TemplateView, Context):
    pass

class RegistrationView(FormView, Context):
    form_class = CreateUserForm
    template_name = 'registration/registration.html'
    success_url = '/mail'


    def form_valid(self, form):
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        phone_number = form.cleaned_data['phone_number']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        data_entry = form.cleaned_data['data_entry']

        valid = validation(email, first_name, last_name, phone_number, password1, password2, data_entry)

        if len(valid) > 0:
            for error in valid:
                form.add_error(error[0], error[1])
                return self.form_invalid(form)

        user = form.save()
        user.save()

        return super(RegistrationView, self).form_valid(form)


def page_not_found_view(request, exception):
    return render(request, 'error.html', status=404)


class BookAPIListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


# Reading elements by category
class BooksApiListCategoryView(ListAPIView):
    serializer_class = BookSerializer
    pagination_class = BookAPIListPagination

    def get_queryset(self):
        sub = self.kwargs['cat']
        category = CategoryModel.objects.filter(sub_slugify1=sub)[0]
        return BooksModel.objects.filter(category=category)


# Reading element
class BooksApiListAllView(ListAPIView):
    serializer_class = BookSerializer
    # permission_classes = (IsAuthenticated,)
    pagination_class = BookAPIListPagination

    def get_queryset(self):
        return cache.get_or_set('all_books', BooksModel.objects.all())


# Reading the element by ID
class BooksApiListIDView(RetrieveAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        if len(BooksModel.objects.filter(id_book=id)) == 0:
            return Response({'error': "Objects does not exist"})
        return BooksModel.objects.filter(id_book=id)


# delete of record
class BooksDestroyView(DestroyAPIView):
    serializer_class = BookSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return  cache.get_or_set('all_books', BooksModel.objects.all())
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('id', None)
        if not id:
            return Response({'error': "method ID not allowed"})

        try:
            instance = BooksModel.objects.get(id_book=id)
            if request.user == instance.creator or request.user.is_superuser:
                instance.delete()

            else:
                return Response({'error': 'You do not have the right to delete this entry'})
        except Exception:
            return Response({'error': 'Objects does not exist'})

        return Response({"post": f"Object {str(id)} is deleted"})



# Update of record
class BooksApiUpdateView(UpdateAPIView):
    serializer_class = BookSerializer
    permission_classes = (IsAdminUser, )

    def put(self, request, *args, **kwargs):
        id = kwargs.get('id', None)
        if not id:
            return Response({'error': "method ID not allowed"})

        try:
            instance = BooksModel.objects.get(id_book=id)

        except Exception:
            return Response({'error': 'Objects does not exist'})

        if request.user != instance.creator and not request.user.is_superuser:
            return Response({'error': "you can't edit this entry"})

        serializer = BookSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data})

    def get_queryset(self):
        return cache.get_or_set('all_books', BooksModel.objects.all())

# Creation of a record
class BooksCreateAPIView(CreateAPIView):
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return cache.get_or_set('all_books', BooksModel.objects.all())



