from rest_framework import serializers

from django.conf import settings
from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        if len(data['students']) > settings.MAX_STUDENTS_PER_COURSE:
            raise serializers.ValidationError('Превышено максимальное количество студентов на курсе.')
        return data
