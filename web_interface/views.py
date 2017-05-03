# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from pymongo import MongoClient
from django.template.response import TemplateResponse
import pprint

databaseName = "BooBook"

client = MongoClient('192.168.32.130', 27017)

db = client[databaseName]


def home(request):
    return TemplateResponse(request, 'index.html')


def orders(request):  # Rendering a speficic order
    return TemplateResponse(request, 'orders.html')


def clients(request):  # Rendering a speficic order
    return TemplateResponse(request, 'clients.html')


def books(request):
    collection = db['books']
    test = collection.find()
    return TemplateResponse(request, 'books.html', {"books": test})


def stats(request):  # Rendering a speficic order
    return TemplateResponse(request, 'stats.html')
