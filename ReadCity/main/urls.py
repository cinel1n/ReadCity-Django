from django.contrib import admin
from django.urls import path, include, re_path
from django.views.decorators.cache import cache_page
from .views import *
from rest_framework import routers
from django.conf.urls import handler404
from django.contrib.auth.urls import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

router = routers.SimpleRouter()

urlpatterns = [
    path('verify/<uuid>', verify, name='verify'),
    path('', HomePageView.as_view(template_name='main.html'), name='home'),
    path('library/<slug:book>', LibraryView.as_view(), name='library'),
    # path('library/<slug:book>', LibraryView.as_view(), name='library'),
    path('bookmark/delete/<int:id>', book_marks_delete, name='delete_bookmark'),
    path('bookmark/delete_all', delete_all_bookmarks, name='delete_all_bookmarks'),
    path('bookmark/add/<int:id>', book_marks_add, name='add_bookmark'),

    path('basket/delete/<int:id>', basket_delete, name='basket_delete'),
    path('basket/add/<int:id>', basket_add, name='basket_add'),

    path('filter/<cat_sort>/<filter>/<direction>/', filter_books, name='book_list_sort'),
    path('registration', RegistrationView.as_view(), name='reg_url'),
    # path('registration/email', BasePage.as_view(template_name='main.html'), name='reg_url'),
    path('login', AuthorizationView.as_view(), name='login_url'),
    path('logout', logout_, name='login_url'),
    path('bookmarks', BookmarksView.as_view(template_name='bookmarks.html'), name='bookmarks'),
    path('my-products', MyProductsView.as_view(template_name='my_products.html'), name='my_products'),
    path('basket', BasketView.as_view(template_name='basket.html'), name='basket'),
    path('book/<int:id>', BookView.as_view(), name='book'),
    # path('book/<int:id>/track_view/', TrackBookView.as_view(), name='track_book_view'),

                  # path('book/<int:id>', BookView.as_view(), name='book'),
    path('search', SearchBookView.as_view(), name='search'),
    path('mail', MailView.as_view(template_name='mail.html')),
    path('api', HomePageView.as_view(template_name='drf_doc.html'), name='api'),
    path('create-entry', CreateBooksView.as_view(), name='create_entry'),

    # path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    path('api/v1/book_list/category/<str:cat>', BooksApiListCategoryView.as_view()),
    path('api/v1/book_list/id/<int:id>', BooksApiListIDView.as_view()),
    path('api/v1/book_list/', BooksApiListAllView.as_view()),

    path('api/v1/book_destroy/<int:id>', BooksDestroyView.as_view()),

    path('api/v1/book_update/<int:id>', BooksApiUpdateView.as_view()),

    path('api/v1/book_create/', BooksCreateAPIView.as_view()),

    path('api/v1/', include(router.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

