from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import Book


class BookTests(TestCase):
    def setUp(self) -> None:
        self.book = Book.objects.create(title='Harry Potter', author='name', price='25.00',)


    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Harry Potter')
        self.assertEqual(f'{self.book.author}', 'name')
        self.assertEqual(f'{self.book.price}', '25.00')

    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_detail_view(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(no_response.status_code, HTTPStatus.NOT_FOUND)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'books/book_detail.html')
 