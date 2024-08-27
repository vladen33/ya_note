from django.contrib.auth import get_user_model
from django.test import TestCase
from http import HTTPStatus

from django.urls import reverse

from notes.models import Note

User = get_user_model()

class TestApp(TestCase):
    def test_mainpage_for_anon_user(self):
        url = reverse('notes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK, (
            'Главная страница недоступна для анонимного пользователя')
        )

    def test_single_note_not_aval_for_anon_user(self):
        user1 = User.objects.create(username='user1')
        note = Note.objects.create(
            title='Заголовок заметки',
            text='Текст заметки',
            slug='slug1',
            author=user1
        )
        url = reverse('notes:detail', kwargs={'slug': note.slug})
        print(f'================== {url} =====================')
        response = self.client.get(url)
        print(f'================== {response} =====================')
        self.assertEqual(response.status_code, HTTPStatus.OK)

