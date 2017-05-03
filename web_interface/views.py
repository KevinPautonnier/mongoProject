# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from pymongo import MongoClient
from datetime import date
from django.template.response import TemplateResponse
import pprint
import datetime
import pytz


databaseName = "BooBook"

client = MongoClient('192.168.117.134', 27017)

db = client[databaseName]
clientsliste = db['clients']
collection = db['books']

def home(request):
    return TemplateResponse(request, 'index.html')


def orders(request):  # Rendering a speficic order
    return TemplateResponse(request, 'orders.html')


def clients(request):  # Rendering a speficic order

    clientrequest = clientsliste.find()
    return TemplateResponse(request, 'clients.html', {"clients": clientrequest})


def books(request):

    test = collection.find()
    return TemplateResponse(request, 'books.html', {"books": test})


def stats(request):  # Rendering a speficic order

    year20 = datetime.timedelta(days = -(20 *365))
    year40 = datetime.timedelta(days = -(40*365))

    vingt = (datetime.datetime.now(pytz.utc) + year20).isoformat()

    quarante = (datetime.datetime.now(pytz.utc) + year40).isoformat()

    print "20"
    print vingt
    print "40"
    print quarante

    client20to40 = clientsliste.find(
        {'birth_date':{'$gt': (vingt), '$lt': (quarante)}}
    )



    # Femme la plus agée

    oldestwomen = clientsliste.find( {'gender' : 'Female', }).sort({ "birth_date" : 1 }).limit(1)




    return TemplateResponse(request, 'stats.html', {"clients": client20to40}, {"oldest" : oldestwomen})
