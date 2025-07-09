import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


with open(settings.BUS_STATION_CSV, newline='', encoding='utf-8') as file:
    data = list(csv.DictReader(file))


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    paginator = Paginator(data, per_page=10)
    current_page = request.GET.get('page', 1)
    page = paginator.get_page(current_page)
    context = {
        'page': page,
        'bus_stations': page.object_list,
    }
    return render(request, 'stations/index.html', context)
