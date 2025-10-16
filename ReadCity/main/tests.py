import unittest
from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.urls import resolve
from main.forms import *
from main.models import CategoryModel

class CatalogTemplateTests(TestCase):
    """    Тест шаблона    """

    def setUp(self):
        url = reverse('reg_url')
        self.response = self.client.get(url)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'registration/registration.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Почта')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Hello World')


class UserFormTests(TestCase):
    """    Тесты для форм    """
    def setUp(self):
        url = reverse('reg_url')
        self.response = self.client.get(url)

    def test_user_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CreateUserForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_book_form_validation_for_blank_items(self):
        add_user = CreateUserForm(
            data={'first_name': '', 'last_name': '', 'phone_number': '', 'email': '', 'password1': '', 'password2': '', 'data_entry' :False }
        )
        self.assertFalse(add_user.is_valid())



class UrlsTest(TestCase):

    def test_main(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_library(self):
        slug_category_list = [i for i in CategoryModel.objects.all()]
        for slug in slug_category_list:

            response = self.client.get(reverse(f'library/{slug}'))
            self.assertEqual(response.status_code, 200)


class CategoryModelTests(TestCase):
    """    Тест модели каталога    """

    def setUp(self):
        self.cat = CategoryModel(
            subcategory1="Новелла",
            subcategory2='',
        )

    def test_create_book(self):
        self.assertIsInstance(self.cat, CategoryModel)

    def test_saving_and_retrieving_book(self):
        first_cat = CategoryModel()
        first_cat.subcategory1 = 'Повесть'
        first_cat.subcategory2 = '-'
        first_cat.save()

        second_cat = CategoryModel()
        second_cat.subcategory1 = 'Роман'
        second_cat.subcategory2 = '-'
        second_cat.save()

        saved_cats = CategoryModel.objects.all()
        self.assertEqual(saved_cats.count(), 2)

        first_saved_cat = saved_cats[0]
        second_saved_cat = saved_cats[1]
        self.assertEqual(first_saved_cat.subcategory1, 'Повесть')
        self.assertEqual(second_saved_cat.subcategory1, 'Роман')


# def setUpModule():
#     print('Running setUpModule')
#
#
# def tearDownModule():
#     print('Running tearDownModule')
#
#
# class TestMyModule(unittest.TestCase):
#     def test_case_1(self):
#         self.assertEqual(5+5, 10)
#
#     def test_case_2(self):
#         self.assertEqual(1+1, 2)