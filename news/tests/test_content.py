"""
1 Количество новостей на главной странице — не более 10.
2 Новости отсортированы от самой свежей к самой старой.
Свежие новости в начале списка.
3 Комментарии на странице отдельной новости отсортированы
от старых к новым: старые в начале списка, новые — в конце.
4 Анонимному пользователю не видна форма для отправки
комментария на странице отдельной новости, а авторизованному видна.
"""

# news/tests/test_content.py
# Импортируем класс формы.
from news.forms import CommentForm
from django.utils import timezone
# Импортируем функцию для получения модели пользователя.
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.conf import settings
from django.test import TestCase
# Импортируем функцию reverse(), она понадобится для получения адреса страницы.
from django.urls import reverse

# Дополнительно к News импортируем модель комментария.
from news.models import Comment, News

User = get_user_model()


class TestHomePage(TestCase):
    # Вынесем ссылку на домашнюю страницу в атрибуты класса.
    HOME_URL = reverse('news:home')

    @classmethod
    def setUpTestData(cls):
        # Можно так:
        # all_news = []
        # for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        #     news = News(title=f'Новость {index}', text='Просто текст.')
        #     all_news.append(news)
        # News.objects.bulk_create(all_news)

        # Вычисляем текущую дату.
        today = datetime.today()
        # Или через list comprehension
        all_news = [
            News(
                title=f'Новость {index}',
                text='Просто текст.',
                # Для каждой новости уменьшаем дату на index дней от today,
                # где index - счётчик цикла.
                date=today - timedelta(days=index)
            )
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        ]
        News.objects.bulk_create(all_news)

        # # или так
        # News.objects.bulk_create(
        #     News(title=f'Новость {index}', text='Просто текст.')
        #     for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        # )

    # Количество новостей на главной странице — не более 10.
    def test_news_count(self):
        # Загружаем главную страницу.
        response = self.client.get(self.HOME_URL)
        # Код ответа не проверяем, его уже проверили в тестах маршрутов.
        # Получаем список объектов из словаря контекста.
        object_list = response.context['object_list']
        # Определяем количество записей в списке.
        news_count = object_list.count()
        # Проверяем, что на странице именно 10 новостей.
        self.assertEqual(news_count, settings.NEWS_COUNT_ON_HOME_PAGE)

    # Тестируем сортировку новостей.
    def test_news_order(self):
        response = self.client.get(self.HOME_URL)
        object_list = response.context['object_list']
        # Получаем даты новостей в том порядке, как они выведены на странице.
        all_dates = [news.date for news in object_list]
        # Сортируем полученный список по убыванию.
        sorted_dates = sorted(all_dates, reverse=True)
        # Проверяем, что исходный список был отсортирован правильно.
        self.assertEqual(all_dates, sorted_dates)


class TestDetailPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(
            title='Тестовая новость', text='Просто текст.'
        )
        # Сохраняем в переменную адрес страницы с новостью:
        cls.detail_url = reverse('news:detail', args=(cls.news.id,))
        cls.author = User.objects.create(username='Комментатор')
        # Запоминаем текущее время:
        now = timezone.now()
        # Создаём комментарии в цикле.
        for index in range(10):
            # Создаём объект и записываем его в переменную.
            comment = Comment.objects.create(
                news=cls.news, author=cls.author, text=f'Tекст {index}',
            )
            # Сразу после создания меняем время создания комментария.
            comment.created = now + timedelta(days=index)
            # И сохраняем эти изменения.
            comment.save()

    # Тестируем сортировку комментариев на странице новости.
    def test_comments_order(self):
        response = self.client.get(self.detail_url)
        # Проверяем, что объект новости находится в словаре контекста
        # под ожидаемым именем - названием модели.
        self.assertIn('news', response.context)
        # Получаем объект новости.
        news = response.context['news']
        # Получаем все комментарии к новости.
        all_comments = news.comment_set.all()
        # Собираем временные метки всех комментариев.
        all_timestamps = [comment.created for comment in all_comments]
        # Сортируем временные метки, менять порядок сортировки не надо.
        sorted_timestamps = sorted(all_timestamps)
        # Проверяем, что временные метки отсортированы правильно.
        self.assertEqual(all_timestamps, sorted_timestamps)

    # Тест наличия формы в словаре контекста:
    # при запросе анонимного пользователя форма
    # не передаётся в словаре контекста.
    def test_anonymous_client_has_no_form(self):
        response = self.client.get(self.detail_url)
        self.assertNotIn('form', response.context)

    # при запросе авторизованного пользователя форма
    # передаётся в словаре контекста.
    def test_authorized_client_has_form(self):
        # Авторизуем клиент при помощи ранее созданного пользователя.
        self.client.force_login(self.author)
        response = self.client.get(self.detail_url)
        self.assertIn('form', response.context)
        # Проверим, что объект формы соответствует нужному классу формы.
        self.assertIsInstance(response.context['form'], CommentForm)
