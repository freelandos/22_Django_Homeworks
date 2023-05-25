import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


data = settings.BUS_STATION_CSV
with open(data, newline='', encoding='utf-8') as csvfile:
    reader = list(csv.DictReader(csvfile))


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    page = int(request.GET.get('page', 1))
    paginator = Paginator(reader, per_page=10)
    current_stations = paginator.get_page(page)
    current_page = paginator.page(page)
    context = {
        'bus_stations': current_stations,
        'page': current_page,
    }
    return render(request, 'stations/index.html', context)
