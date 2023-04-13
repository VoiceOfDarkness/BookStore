from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from .models import Book, Review


class BookTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(username='reviewuser', email='reviewuser@gmail.com', password='admin12345')
        self.special_permission = Permission.objects.get(codename='special_status')
        self.book = Book.objects.create(title='Harry Potter', author='name', price='25.00',)
        self.review = Review.objects.create(book = self.book, author=self.user, review = 'Nice!',)

    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Harry Potter')
        self.assertEqual(f'{self.book.author}', 'name')
        self.assertEqual(f'{self.book.price}', '25.00')

    def test_book_list_view_for_logged_in_user(self):
        self.client.login(email='reviewuser@gmail', password='admin12345')
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'books/book_list.html')
        
    def test_book_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, '%s?next=/books/'% (reverse('account_login')))
        response = self.client.get('%s?next=/books/' % (reverse('account_login')))
        self.assertNotContains(response, 'Log OIn')

    def test_book_detail_view_with_permissions(self):
        self.client.login(email='reviewuser@gmail.com', password='admin12345',)
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book.get_absolute_url)
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(no_response.status_code, HTTPStatus.NOT_FOUND)
        self.assertContains(response, 'Harry Potter')
        self.assertContains(response, 'An excellent Potter')
        self.assertTemplateUsed(response, 'books/book_detail.html')

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
        self.assertContains(response, 'Nice!')
        self.assertTemplateUsed(response, 'books/book_detail.html')
 