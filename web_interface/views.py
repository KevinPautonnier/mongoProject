# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from pymongo import MongoClient
from django.template.response import TemplateResponse
import pprint

databaseName = "test"

client = MongoClient('192.168.255.128', 27017)

db = client[databaseName]
collection = db['csv']

test = collection.find_one()

pprint.pprint(test)


def home(request):
    return TemplateResponse(request, 'index.html')
