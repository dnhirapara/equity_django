from django.shortcuts import render

# Create your views here.

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.conf import settings
from daily_data.api.utils import *

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def home(request):
    context = {}
    name = "Hello World!!! from db"
    context['name'] = name
    filename = get_zip()
    date = parse_date(filename)
    eq_day, eq_month, eq_year = parse_date(filename)
    data = read_csv_data(eq_day, eq_month, eq_year)
    context['data'] = data
    context['date'] = date
    for i in range(1, len(data)):
        row_list = [data[i][1], data[i][4], data[i][5], data[i][6], data[i][7]]
        cache.set(data[i][1], row_list)
        # print(cache.get(data[i][1]))
    context['list'] = cache.keys('*ABB*')
    print(context['list'])
    cache.set('name', 'Darshik_H from cache')
    if cache.get('name'):
        context['name'] = cache.get('name')
    else:
        for i in range(1, len(data)):
            row_list = [data[2], data[3]]
            cache.set(data[0], row_list)
            print(cache.get(data[0]))
        context['list'] = cache.get(data[1][1])
        cache.set('name', 'Darshik_H from cache')
    return render(request, 'home.html', context)
