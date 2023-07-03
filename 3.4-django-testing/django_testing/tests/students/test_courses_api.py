import pytest
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from django.urls import reverse

from students.models import Course


@pytest.mark.django_db
def test_get_first_course(api_client, course_factory):
    """Получение первого курса."""

    course = course_factory()
    url = reverse('courses-detail', args=[course.id])

    response = api_client.get(url)
    data = response.json()

    assert response.status_code == HTTP_200_OK
    assert data['name'] == course.name


@pytest.mark.django_db
def test_get_courses_list(api_client, course_factory):
    """Получение списка курсов."""

    courses = course_factory(_quantity=10)
    url = reverse('courses-list')

    response = api_client.get(url)
    data = response.json()

    assert response.status_code == HTTP_200_OK
    assert len(data) == len(courses)
    for i, course in enumerate(data):
        assert course['name'] == courses[i].name


@pytest.mark.django_db
def test_filter_courses_list_by_id(api_client, course_factory):
    """Фильтрация списка курсов по id."""

    courses = course_factory(_quantity=10)
    filter_data = {'id': courses[0].id}
    url = reverse('courses-list')

    response = api_client.get(url, data=filter_data)
    data = response.json()

    assert response.status_code == HTTP_200_OK
    assert len(data) == 1
    assert data[0]['id'] == courses[0].id


@pytest.mark.django_db
def test_filter_courses_list_by_name(api_client, course_factory):
    """Фильтрация списка курсов по name."""

    courses = course_factory(_quantity=10)
    filter_data = {'name': courses[0].name}
    url = reverse('courses-list')

    response = api_client.get(url, data=filter_data)
    data = response.json()

    assert response.status_code == HTTP_200_OK
    assert len(data) == 1
    assert data[0]['name'] == courses[0].name


@pytest.mark.django_db
def test_create_course(api_client):
    """Создание курса."""

    course_data = {'name': 'test_name', 'students': []}
    count = Course.objects.count()
    url = reverse('courses-list')

    response = api_client.post(url, data=course_data)
    data = response.json()

    assert response.status_code == HTTP_201_CREATED
    assert Course.objects.count() == count + 1
    assert data['name'] == 'test_name'
    assert data['students'] == []


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    """Обновление курса."""

    course = course_factory()
    course_data = {'name': 'new_name', 'students': []}
    url = reverse('courses-detail', args=[course.id])

    response = api_client.patch(url, data=course_data)
    data = response.json()

    assert response.status_code == HTTP_200_OK
    assert data['name'] == 'new_name'
    assert data['students'] == []


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    """Удаление курса."""

    course = course_factory()
    count = Course.objects.count()
    url = reverse('courses-detail', args=[course.id])

    response = api_client.delete(url)

    assert response.status_code == HTTP_204_NO_CONTENT
    assert Course.objects.count() == count - 1


@pytest.mark.parametrize('students_count, expected_status', [
    (19, HTTP_201_CREATED),
    (20, HTTP_201_CREATED),
    (21, HTTP_400_BAD_REQUEST),
])
@pytest.mark.django_db
def test_limit_create_students(api_client, student_factory, settings,
                               students_count, expected_status):
    """Максимальное количество студентов на курсе."""

    settings.MAX_STUDENTS_PER_COURSE = 20
    students = student_factory(_quantity=students_count)
    students_ids = [student.id for student in students]
    course_data = {'name': 'test_name', 'students': students_ids}
    count = Course.objects.count()
    url = reverse('courses-list')

    response = api_client.post(url, data=course_data)
    data = response.json()

    assert response.status_code == expected_status
    if response.status_code == HTTP_201_CREATED:
        assert Course.objects.count() == count + 1
        assert data['name'] == 'test_name'
        assert len(data['students']) == students_count
        assert data['students'] == students_ids
    else:
        assert Course.objects.count() == count
