from http import HTTPStatus

from notes.tests.fixtures import (NotesFixturesTestCase, URL_ADD, URL_EDIT,
                                  URL_DELETE, URL_DETAIL, URL_HOME, URL_LIST,
                                  URL_LOGIN, URL_LOGOUT, URL_SIGNUP,
                                  URL_SUCCESS)


class TestRoutes(NotesFixturesTestCase):
    def test_pages_availability(self):
        data = (
            (URL_HOME, self.client, HTTPStatus.OK),
            (URL_LOGIN, self.client, HTTPStatus.OK),
            (URL_LOGOUT, self.client, HTTPStatus.OK),
            (URL_SIGNUP, self.client, HTTPStatus.OK),
            (URL_LIST, self.not_author_client, HTTPStatus.OK),
            (URL_SUCCESS, self.not_author_client, HTTPStatus.OK),
            (URL_ADD, self.not_author_client, HTTPStatus.OK),
            (URL_DETAIL, self.author_client, HTTPStatus.OK),
            (URL_EDIT, self.author_client, HTTPStatus.OK),
            (URL_DELETE, self.author_client, HTTPStatus.OK),
            (URL_DETAIL, self.not_author_client, HTTPStatus.NOT_FOUND),
            (URL_EDIT, self.not_author_client, HTTPStatus.NOT_FOUND),
            (URL_DELETE, self.not_author_client, HTTPStatus.NOT_FOUND),
        )
        for url, client, status in data:
            with self.subTest(url=url, client=client, status=status):
                response = client.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirect(self):
        url_names = (URL_LIST, URL_ADD, URL_SUCCESS,
                     URL_DETAIL, URL_EDIT, URL_DELETE)
        for url in url_names:
            with self.subTest(url=url):
                expected_url = f'{URL_LOGIN}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, expected_url)
