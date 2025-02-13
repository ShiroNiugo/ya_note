# test_routes.py
import pytest
from http import HTTPStatus

from django.urls import reverse


# # Указываем в фикстурах встроенный клиент.
# def test_home_availability_for_anonymous_user(client):
#     # Адрес страницы получаем через reverse():
#     url = reverse('notes:home')
#     response = client.get(url)
#     assert response.status_code == HTTPStatus.OK


# @pytest.mark.parametrize(
#     'name',  # Имя параметра функции.
#     # Значения, которые будут передаваться в name.
#     ('notes:home', 'users:login', 'users:logout', 'users:signup')
# )
# # Указываем имя изменяемого параметра в сигнатуре теста.
# def test_pages_availability_for_anonymous_user(client, name):
#     url = reverse(name)  # Получаем ссылку на нужный адрес.
#     response = client.get(url)  # Выполняем запрос.
#     assert response.status_code == HTTPStatus.OK


# @pytest.mark.parametrize(
#     'name',
#     ('notes:list', 'notes:add', 'notes:success')
# )
# def test_pages_availability_for_auth_user(admin_client, name):
#     url = reverse(name)
#     response = admin_client.get(url)
#     assert response.status_code == HTTPStatus.OK 


# @pytest.mark.parametrize(
#     'name',
#     ('notes:list', 'notes:add', 'notes:success')
# )
# def test_pages_availability_for_auth_user(not_author_client, name):
#     url = reverse(name)
#     response = not_author_client.get(url)
#     assert response.status_code == HTTPStatus.OK


# from notes.models import Note


# def test_note_exists(note):
#     notes_count = Note.objects.count()
#     # Общее количество заметок в БД равно 1.
#     assert notes_count == 1
#     # Заголовок объекта, полученного при помощи фикстуры note,
#     # совпадает с тем, что указан в фикстуре.
#     assert note.title == 'Заголовок'


# # Обозначаем, что тесту нужен доступ к БД. 
# # Без этой метки тест выдаст ошибку доступа к БД.
# @pytest.mark.django_db
# def test_empty_db():
#     notes_count = Note.objects.count()
#     # В пустой БД никаких заметок не будет:
#     assert notes_count == 0


# # Параметризуем тестирующую функцию:
# @pytest.mark.parametrize(
#     'name',
#     ('notes:detail', 'notes:edit', 'notes:delete'),
# )
# def test_pages_availability_for_author(author_client, name, note):
#     url = reverse(name, args=(note.slug,))
#     response = author_client.get(url)
#     assert response.status_code == HTTPStatus.OK


# # Добавляем к тесту ещё один декоратор parametrize; в его параметры
# # нужно передать фикстуры-клиенты и ожидаемый код ответа для каждого клиента.
# @pytest.mark.parametrize(
#     # parametrized_client - название параметра, 
#     # в который будут передаваться фикстуры;
#     # Параметр expected_status - ожидаемый статус ответа.
#     'parametrized_client, expected_status',
#     # В кортеже с кортежами передаём значения для параметров:
#     (
#         (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
#         (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
#     ),
# )
# # Этот декоратор оставляем таким же, как в предыдущем тесте.
# @pytest.mark.parametrize(
#     'name',
#     ('notes:detail', 'notes:edit', 'notes:delete'),
# )
# # В параметры теста добавляем имена parametrized_client и expected_status.
# def test_pages_availability_for_different_users(
#         parametrized_client, name, note, expected_status
# ):
#     url = reverse(name, args=(note.slug,))
#     # Делаем запрос от имени клиента parametrized_client:
#     response = parametrized_client.get(url)
#     # Ожидаем ответ страницы, указанный в expected_status:
#     assert response.status_code == expected_status

from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name, args',
    (
        ('notes:detail', pytest.lazy_fixture('slug_for_args')),
        ('notes:edit', pytest.lazy_fixture('slug_for_args')),
        ('notes:delete', pytest.lazy_fixture('slug_for_args')),
        ('notes:add', None),
        ('notes:success', None),
        ('notes:list', None),
    ),
)
# Передаём в тест анонимный клиент, name проверяемых страниц и args:
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    # Теперь не надо писать никаких if и можно обойтись одним выражением.
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
