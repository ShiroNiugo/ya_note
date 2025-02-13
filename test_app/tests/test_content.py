from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note
from notes.forms import NoteForm


User   = get_user_model()


class TestContent(TestCase):
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
        cls.note2 = Note.objects.create(
            title='Заголовок2',
            text='Текст2',
            slug='default2',
            author=cls.author2,
        )

    def test_note_in_object_list(self):
        url = reverse('notes:list')
        response = self.client.get(url)
        object_list = response.context['object_list']
        self.assertIn(self.note1, object_list)
        self.assertIn(self.note2, object_list)

    def test_note_in_object_list_by_author(self):
        self.client.force_login(self.author1)
        url = reverse('notes:list')
        response = self.client.get(url)
        object_list = response.context['object_list']
        self.assertIn(self.note1, object_list)
        self.assertNotIn(self.note2, object_list)

    def test_note_form_in_create_page(self):
        self.client.force_login(self.author1)
        url = reverse('notes:add')
        response = self.client.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_note_form_in_edit_page(self):
        self.client.force_login(self.author1)
        url = reverse('notes:edit', args=(self.note1.slug,))
        response = self.client.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
