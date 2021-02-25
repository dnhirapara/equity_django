import csv
import os
import shutil
import time
from datetime import date, datetime
from zipfile import ZipFile

import redis
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from celery import shared_task

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def redis_con():
    return redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


URL = "https://www.bseindia.com/markets/marketinfo/BhavCopy.aspx"


def data_from_zip(filepath):
    try:
        with ZipFile(filepath, 'r') as zipfile:
            zipfile.printdir()
            csv_filepath = settings.CSV_FOLDER
            print(csv_filepath)
            r = zipfile.extractall(path=csv_filepath)
    except FileNotFoundError:
        print("File Not Found!!!")


def read_csv_data(eq_day, eq_month, eq_year):
    filename = "EQ"+str(eq_day)+str(eq_month)+str(eq_year)+".CSV"
    csv_filepath = os.path.join(settings.CSV_FOLDER, filename)
    with open(csv_filepath, 'r') as f:
        reader = csv.reader(f)
        list_data = []
        for row in reader:
            list_data.append(row)
            # print(row)
        return list_data


def parse_date(filepath):
    ind = 0
    for i in range(len(filepath)):
        if '/' == filepath[i]:
            ind = i+1
    filename = filepath[ind:]
    eq_day = filename[2: 4]
    eq_month = filename[4: 6]
    eq_year = filename[6: 8]
    return eq_day, eq_month, eq_year


def get_zip():

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    web_page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(web_page.text, "html.parser")

    equity_zip_link = soup.find(id='ContentPlaceHolder1_btnhylZip').get('href')
    print(equity_zip_link)
    ind = 0
    for i in range(len(equity_zip_link)):
        if '/' == equity_zip_link[i]:
            ind = i+1
    file_name = equity_zip_link[ind:]
    print(file_name)
    zip_file = requests.get(equity_zip_link, headers=headers)

    dir_path = settings.ZIP_FOLDER
    with open(os.path.join(dir_path, file_name), 'wb') as f:
        f.write(zip_file.content)

    data_from_zip(os.path.join(dir_path, file_name))
    return file_name


def clear_cache(conn, prefix):
    count = 0
    for key in conn.scan_iter(str(prefix)+"*"):
        cache.delete(key)
        count += 1
    return count

def wait_until_currunt_day(day, month, year):
    today_date = date.today()
    wait_secs = 300
    while day != today_date.day or month != today_date.month or year != today_date.year:
        time.sleep(60)
        file_name = get_zip()
        day, month, year = parse_date(file_name)
        wait_secs -= 60
        if wait_secs < 0:
            return 0

@shared_task
def sample_task():

    today_date = date.today()
    file_name = get_zip()
    day, month, year = parse_date(file_name)
    # day, month, year = wait_until_currunt_day(day, month, year)
    
    shutil.rmtree(settings.MEDIA_ROOT)
    os.mkdir(settings.MEDIA_ROOT)

    csv_data = read_csv_data(day, month, year)
    parsed_date = datetime(year=int(str(20)+str(year)),
                           month=int(month), day=int(day))
    redis_cache = redis_con()
    clear_cache(redis_cache, "id")
    redis_cache.delete("date")
    redis_cache.set("date", str(datetime.now()))
    print(redis_cache.get('date'))
    total = 0
    for i in range(1, len(csv_data)):
        total += 1
        row_list = [csv_data[i][1], csv_data[i][4],
                    csv_data[i][5], csv_data[i][6], csv_data[i][7]]
        redis_cache.delete("id:"+csv_data[i][0]+":"+csv_data[i][1])
        redis_cache.rpush(
            "id:"+csv_data[i][0]+":"+csv_data[i][1], *row_list)
        redis_cache.persist("id:"+csv_data[i][0])
    return total
