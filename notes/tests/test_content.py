from notes.forms import NoteForm
from notes.tests.fixtures import (NotesFixturesTestCase, URL_ADD, URL_EDIT,
                                  URL_LIST)


class TestContent(NotesFixturesTestCase):
    def test_note_in_list_for_author(self):
        response = TestContent.author_client.get(URL_LIST)
        object_list = response.context['object_list']
        self.assertIn(TestContent.note, object_list)

    def test_note_not_in_list_for_another_user(self):
        response = TestContent.not_author_client.get(URL_LIST)
        object_list = response.context['object_list']
        self.assertNotIn(TestContent.note, object_list)

    def test_create_note_page_contains_form(self):
        response = TestContent.author_client.get(URL_ADD)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_edit_note_page_contains_form(self):
        response = TestContent.author_client.get(URL_EDIT)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
