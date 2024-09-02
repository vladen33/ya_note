from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.fixtures import (NotesFixturesTestCase, URL_ADD, URL_EDIT,
                                  URL_DELETE, URL_LOGIN, URL_SUCCESS)


class TestLogic(NotesFixturesTestCase):
    def setUp(self):
        self.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }

    def test_user_can_create_note(self):
        count_before = Note.objects.count()
        response = self.author_client.post(URL_ADD, self.form_data)
        count_after = Note.objects.count()
        self.assertEqual(count_after - count_before, 1)
        self.assertRedirects(response, URL_SUCCESS)
        new_note = Note.objects.order_by('pk').last()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        count_before = Note.objects.count()
        response = self.client.post(URL_ADD, self.form_data)
        count_after = Note.objects.count()
        self.assertEqual(count_after - count_before, 0)
        expected_url = f'{URL_LOGIN}?next={URL_ADD}'
        self.assertRedirects(response, expected_url)

    def test_not_unique_slug(self):
        count_before = Note.objects.count()
        self.author_client.post(URL_ADD, data=self.form_data)
        response = self.author_client.post(URL_ADD, data=self.form_data)
        count_after = Note.objects.count()
        self.assertEqual(count_after - count_before, 1)
        self.assertFormError(response, 'form', 'slug',
                             errors=(self.form_data['slug'] + WARNING)
                             )

    def test_empty_slug(self):
        self.form_data.pop('slug')
        count_before = Note.objects.count()
        response = self.author_client.post(URL_ADD, data=self.form_data)
        count_after = Note.objects.count()
        self.assertEqual(count_after - count_before, 1)
        self.assertRedirects(response, URL_SUCCESS)
        new_note = Note.objects.order_by('pk').last()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        response = self.author_client.post(URL_EDIT, self.form_data)
        self.assertRedirects(response, URL_SUCCESS)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.form_data['title'])
        self.assertEqual(self.note.text, self.form_data['text'])
        self.assertEqual(self.note.slug, self.form_data['slug'])

    def test_other_user_can_edit_note(self):
        response = self.not_author_client.post(URL_EDIT, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)

    def test_author_can_delete_node(self):
        count_before = Note.objects.count()
        response = self.author_client.post(URL_DELETE)
        count_after = Note.objects.count()
        self.assertEqual(count_before - count_after, 1)
        self.assertRedirects(response, URL_SUCCESS)

    def test_other_user_cant_delete_node(self):
        count_before = Note.objects.count()
        response = self.not_author_client.post(URL_DELETE)
        count_after = Note.objects.count()
        self.assertEqual(count_after - count_before, 0)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
