from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()

SLUG = 'note-slug'
URL_ADD = reverse('notes:add')
URL_DELETE = reverse('notes:delete', kwargs={'slug': SLUG})
URL_DETAIL = reverse('notes:detail', kwargs={'slug': SLUG})
URL_EDIT = reverse('notes:edit', kwargs={'slug': SLUG})
URL_HOME = reverse('notes:home')
URL_LIST = reverse('notes:list')
URL_LOGIN = reverse('users:login')
URL_LOGOUT = reverse('users:logout')
URL_SIGNUP = reverse('users:signup')
URL_SUCCESS = reverse('notes:success')


class NotesFixturesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.not_author = User.objects.create(username='Читатель')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug=SLUG,
            author=cls.author
        )
