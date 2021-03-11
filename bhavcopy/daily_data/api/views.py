from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
import json
import os
import redis
import csv


def redis_con():
    return redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


@api_view(['GET'])
def get_demo(request):
    if request.method == 'GET':
        return Response({"name": "server"}, status=200)


@api_view(['GET'])
def get_list(request):
    if request.method == 'GET':

        limit = request.query_params.get('limit')
        search = request.query_params.get('search')
        offset = request.query_params.get('offset')

        redis_cache = redis_con()

        if search is None:
            search = "id:*"
        else:
            search = "id:*"+str(search).upper() + "*"

        redis_keys = redis_cache.keys(search)

        if offset is None or int(offset) >= len(redis_keys):
            offset = 0
        else:
            offset = int(offset)

        if limit is None:
            limit = len(redis_keys)
        else:
            limit = min(int(limit), len(redis_keys))

        print("limit : "+str(limit))
        data = []
        k = 0
        total = 0
        for i in range(offset, limit):
            total += 1
            keys = redis_keys[i].decode('utf-8')
            redis_data = redis_cache.lrange(keys, 0, -1)
            row_data = {}
            col_data = ["NAME", "OPEN", "HIGH", "LOW", "CLOSE"]
            for i in range(len(redis_data)):
                row_data[col_data[i]] = str(
                    redis_data[i].decode('utf-8')).strip()
            data.append(row_data)
        response = {
            'data': data,
            'total': total,
            'date': redis_cache.get('date'),
            'entire_total':len(redis_keys)
        }
        return Response(response, status=200)


@api_view(['GET'])
def get_csv(request, key):
    if request.method == 'GET':

        redis_cache = redis_con()
        redis_keys = redis_cache.keys("id:*"+str(key).upper() + "*")

        key = str(key).lower()
        file_name = key
        if file_name == '*':
            file_name = 'alldata'
        file_path = os.path.join(settings.MEDIA_ROOT, file_name+'.csv')

        if os.path.exists(file_path):
            return Response({'url': request.get_host() + settings.MEDIA_URL+file_name+'.csv'}, status=200)

        elif 0 == len(redis_keys):
            return Response({"error": "No Data containing '"+key+"'"}, status=200)

        else:
            with open(file_path, mode='w') as equity_file:
                equity_file = csv.writer(
                    equity_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                equity_file.writerow(["NAME", "OPEN", "HIGH", "LOW", "CLOSE"])

                for i in range(len(redis_keys)):
                    keys = redis_keys[i].decode('utf-8')
                    redis_data = redis_cache.lrange(keys, 0, -1)
                    row_data = [str(i.decode('utf-8')).strip()
                                for i in redis_data]
                    equity_file.writerow(row_data)

            print(request.get_host())
            return Response({'url': request.get_host() + settings.MEDIA_URL+file_name+'.csv'}, status=200)
