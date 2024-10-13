from django.shortcuts import render,get_object_or_404, get_list_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
# import requests
import json
from .forms import SearchForm, ResultForm
from .models import Result
import urllib.request



@api_view(['GET'])
def words(requests):
    encText = urllib.parse.quote("사과")
    url = 'https://openapi.naver.com/v1/search/encyc.json?query='+encText

    client_id = "KvPVSmEYFy8fKI9lXDZO"
    client_secret = "wWqDqnznwW" 
    
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    response_body = response.read()
    rescode = response.getcode()
    
    items = json.loads(response_body)['items']

    new_list = []

    for item in items :
        new_data = {'model' : 'apidb.word'}
        dic_list = {}

        dic_list['title'] = item['title']
        dic_list['description'] = item['description']

        new_data['fields'] = dic_list

        new_list.append(new_data)

    if(rescode==200):
        with open('word.json', 'w', encoding='UTF-8') as f:
            json.dump(new_list, f, ensure_ascii=False, indent=2)
    else:
        print("Error Code:" + rescode)

    return Response(response_body)


