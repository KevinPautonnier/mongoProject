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
        {'birth_date':{'$gt': (quarante), '$lt': (vingt)}}
    )

    """for i in client20to40:
        print i["birth_date"]

    #Nb adrese mail avec chiffres

    emailnumber = clientsliste.find()
    nbadresse = 0
    for email in emailnumber :
        #print email["email"]

        if "0" in list(str(email["email"]))or "1" in list(str(email["email"]))or "2" in list(str(email["email"]))or "3" in list(str(email["email"]))or "4" in list(str(email["email"]))or"5" in list(str(email["email"]))or "6" in list(str(email["email"]))or "7" in list(str(email["email"]))or "8" in list(str(email["email"]))or "9" in list(str(email["email"])):
            nbadresse += 1

    print nbadresse

    #Femme la plus agée

    # oldestwomen = clientsliste.find( {'gender' : 'Female', }).sort({ "birth_date" : 1 }).limit(1)"""

    return TemplateResponse(request, 'stats.html', {"stats": client20to40})


