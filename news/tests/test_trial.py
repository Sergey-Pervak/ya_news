# # news/tests/test_trial.py
# from django.test import TestCase


# class Test(TestCase):

#     def test_example_success(self):
#         self.assertTrue(True)  # Этот тест всегда будет проходить успешно.


# class YetAnotherTest(TestCase):

#     def test_example_fails(self):
#         self.assertTrue(False)  # Этот тест всегда будет проваливаться.


# news/tests/test_trial.py
# Импортируем функцию для определения модели пользователя.
# from django.contrib.auth import get_user_model
# from django.test import Client, TestCase
# import unittest

# # Импортируем модель, чтобы работать с ней в тестах.
# from news.models import News

# # Получаем модель пользователя.
# User = get_user_model()


# # Создаём тестовый класс с произвольным названием, наследуем его от TestCase.
# @unittest.skip('Этот тест мы просто пропускаем')
# class TestNews(TestCase):
#     # Все нужные переменные сохраняем в атрибуты класса.
#     TITLE = 'Заголовок новости'
#     TEXT = 'Тестовый текст'

#     # В методе класса setUpTestData создаём тестовые объекты.
#     # Оборачиваем метод соответствующим декоратором.
#     @classmethod
#     def setUpTestData(cls):
#         # Стандартным методом Django ORM create() создаём объект класса.
#         # Присваиваем объект атрибуту класса: назовём его news.
#         cls.news = News.objects.create(
#             # При создании объекта обращаемся к константам класса через cls.
#             title=cls.TITLE,
#             text=cls.TEXT,
#         )

#         # Создаём пользователя.
#         cls.user = User.objects.create(username='testUser')
#         # Создаём объект клиента.
#         cls.user_client = Client()
#         # "Логинимся" в клиенте при помощи метода force_login().
#         cls.user_client.force_login(cls.user)
#         # Теперь через этот клиент можно отправлять запросы
#         # от имени пользователя с логином "testUser".

#     # Проверим, что объект действительно было создан.
#     # @unittest.skip('Этот тест мы просто пропускаем')
#     def test_successful_creation(self):
#         # При помощи обычного ORM-метода посчитаем количество записей в базе.
#         news_count = News.objects.count()
#         # Сравним полученное число с единицей.
#         self.assertEqual(news_count, 1)

#     # @unittest.skip('Этот тест мы просто пропускаем')
#     def test_title(self):
#         # Сравним свойство объекта и ожидаемое значение.
#         # Чтобы проверить равенство с константой -
#         # обращаемся к ней через self, а не через cls:
#         self.assertEqual(self.news.title, self.TITLE)
