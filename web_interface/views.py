# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from pymongo import MongoClient
from datetime import date
from django.template.response import TemplateResponse
import pprint
import datetime
import pytz
import pymongo
databaseName = "BooBook"

client = MongoClient('192.168.152.133', 27017)

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

    client20to40 = clientsliste.find(
        {'gender' : 'Male', 'birth_date':{'$gt': (quarante), '$lt': (vingt)}}
    )

    #Femme la plus agée

    oldestwomen = clientsliste.find({'gender': 'Female'}).sort('birth_date', pymongo.ASCENDING).limit(1)

    mailnumber = clientsliste.find()
    test = 0
    liste = []
    print type(mailnumber)
    for mail in mailnumber:
        if '0' in str(mail["email"]) or '1' in str(mail["email"]) or '2' in str(mail["email"]) or '3' in str(mail["email"]) or '4' in str(mail["email"]) or '5' in str(mail["email"]) or '6' in str(mail["email"]) or '7' in str(mail["email"]) or '8' in str(mail["email"]) or '9' in str(mail["email"]):
            test = test + 1
            liste.append(mail)
        else:
            print mail["email"]
    print test
    return TemplateResponse(request, 'stats.html', {"femmes": oldestwomen, "stats": client20to40, "mails": liste})