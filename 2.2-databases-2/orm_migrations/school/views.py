from django.views.generic import ListView
from django.shortcuts import render

from school.models import Student


def students_list(request):
    template = 'school/students_list.html'
    students = Student.objects.order_by('group').prefetch_related('teachers')
    context = {
        'students': students
    }
    return render(request, template, context)
