from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note
from pytils.translit import slugify


User = get_user_model()


class TestLogic(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author1 = User.objects.create(username='Лев Толстой')
        cls.author2 = User.objects.create(username='Читатель простой')
        cls.note1 = Note.objects.create(
            title='Заголовок1',
            text='Текст1',
            slug='default1',
            author=cls.author1,
        )

    def test_authenticated_user_can_create_note(self):
        self.client.force_login(self.author1)
        url = reverse('notes:add')
        data = {'title': 'Заголовок', 'text': 'Текст'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Note.objects.count(), 2)

    def test_anonymous_user_cannot_create_note(self):
        url = reverse('notes:add')
        data = {'title': 'Заголовок', 'text': 'Текст'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Note.objects.count(), 1)

    def test_cannot_create_two_notes_with_same_slug(self):
        self.client.force_login(self.author1)
        url = reverse('notes:add')
        data = {'title': 'Заголовок', 'text': 'Текст', 'slug': 'default1'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 1)

    def test_slug_is_generated_automatically(self):
        self.client.force_login(self.author1)
        url = reverse('notes:add')
        data = {'title': 'Заголовок', 'text': 'Текст'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        note = Note.objects.get(title='Заголовок')
        self.assertEqual(note.slug, slugify('Заголовок'))

    def test_user_can_edit_own_note(self):
        self.client.force_login(self.author1)
        url = reverse('notes:edit', args=(self.note1.slug,))
        data = {'title': 'Новый заголовок', 'text': 'Новый текст'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        note = Note.objects.get(slug=self.note1.slug)
        self.assertEqual(note.title, 'Новый заголовок')
        self.assertEqual(note.text, 'Новый текст')

    def test_user_cannot_edit_foreign_note(self):
        self.client.force_login(self.author2)
        url = reverse('notes:edit', args=(self.note1.slug,))
        data = {'title': 'Новый заголовок', 'text': 'Новый текст'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)
        note = Note.objects.get(slug=self.note1.slug)
        self.assertEqual(note.title, 'Заголовок1')
        self.assertEqual(note.text, 'Текст1')

    def test_user_can_delete_own_note(self):
        self.client.force_login(self.author1)
        url = reverse('notes:delete', args=(self.note1.slug,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Note.objects.count(), 0)

    def test_user_cannot_delete_foreign_note(self):
        self.client.force_login(self.author2)
        url = reverse('notes:delete', args=(self.note1.slug,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Note.objects.count(), 1)
