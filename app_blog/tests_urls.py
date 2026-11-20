from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import timezone
from .models import Category, Article
from .views import (
    HomePageView,
    ArticleList,
    ArticleCategoryList,
    ArticleDetail,
)


class HomeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            category='Advertising',
            slug='advertising',
        )
        cls.pub_date = timezone.now()
        cls.article = Article.objects.create(
            title='Test Campaign',
            description='Test description',
            pub_date=cls.pub_date,
            slug='test-campaign',
            main_page=True,
            category=cls.category,
        )

    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func.view_class, HomePageView)

    def test_articles_list_view_status_code(self):
        url = reverse('articles-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_articles_list_url_resolves_view(self):
        view = resolve('/articles')
        self.assertEqual(view.func.view_class, ArticleList)

    def test_category_view_status_code(self):
        url = reverse('articles-category-list', args=('advertising',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_category_url_resolves_view(self):
        view = resolve('/articles/category/advertising')
        self.assertEqual(view.func.view_class, ArticleCategoryList)

    def test_article_detail_view_status_code(self):
        url = reverse(
            'news-detail',
            args=(
                self.pub_date.strftime('%Y'),
                self.pub_date.strftime('%m'),
                self.pub_date.strftime('%d'),
                'test-campaign',
            ),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_article_detail_url_resolves_view(self):
        view = resolve('/articles/2026/11/20/test-campaign')
        self.assertEqual(view.func.view_class, ArticleDetail)
