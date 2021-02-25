# Create your views here.
from bs4 import BeautifulSoup
import csv
import requests
import redis
import os
from zipfile import ZipFile
import csv


def redis_con():
    return redis.Redis(host='localhost', port=6379, db=0)


URL = "https://www.bseindia.com/markets/marketinfo/BhavCopy.aspx"


def data_from_zip(filepath):
    try:
        with ZipFile(filepath, 'r') as zipfile:
            zipfile.printdir()
            csv_filepath = './csv_files/'
            r = zipfile.extractall(path=csv_filepath)
    except FileNotFoundError:
        print("File Not Found!!!")


def read_csv_data(eq_day, eq_month, eq_year):
    filename = "EQ"+str(eq_day)+str(eq_month)+str(eq_year)+".CSV"
    csv_filepath = "./csv_files/"+filename
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
    # Write content to file
    # r = redis_con()
    # r.set('zip_name', 'Timepass')
    # print(r.get('zip_name'))
    dir_path = './zips/'
    with open(dir_path+file_name, 'wb') as f:
        f.write(zip_file.content)

    data_from_zip(dir_path + file_name)
    return file_name
    # eq_day, eq_month, eq_year = parse_date(file_name)
    # read_csv_data(eq_day, eq_month, eq_year)
