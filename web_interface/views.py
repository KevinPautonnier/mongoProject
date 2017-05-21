# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from pymongo import MongoClient
from datetime import date
from django.template.response import TemplateResponse
import pprint
import datetime
import pytz
from bson.objectid import ObjectId
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

    if request.method == 'POST':
        form = request.POST
        if form['action'] == 'put':
            clientsliste.insert({
                'gender': 'Male',
                'first_name': form['first_name'],
                'last_name': form['last_name'],
                'registration_date': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                'email': form['email'],
                'birth-date': form['birth_date']
        })
        elif form['action'] == 'delete':
            clientsliste.delete_one(
                {
                    '_id': ObjectId(form['id'])
                }
            )
        elif form['action'] == 'edit':
            clientsliste.update(
                {"_id": ObjectId(form['id'])},
                {
                    "$set": {
                        'gender': 'Male',
                        'first_name': form['first_name'],
                        'last_name': form['last_name'],
                        'email': form['email'],
                        'birth-date': form['birth_date']
                    }
                }
            )

    clientrequest = clientsliste.find()
    return TemplateResponse(request, 'clients.html', {"clients": clientrequest})


def edit_client(request):

    form = request.POST

    client = clientsliste.find_one({
        '_id':  ObjectId(form['id'])
    })

    print client

    return TemplateResponse(request, 'form/edit_client.html', {"client": client})


def books(request):

    print 'books'

    if request.method == 'POST':
        form = request.POST
        if form['action'] == 'put':
            collection.insert({
                'name': form['name'],
                'author_name': form['author_name'],
                'book_date_added': form['book_date_added'],
                'isbn': form['isbn'],
                'price': form['price']
        })
        elif form['action'] == 'delete':
            collection.delete_one(
                {
                    '_id': ObjectId(form['id'])
                }
            )
        elif form['action'] == 'edit':
            collection.update(
                {"_id": ObjectId(form['id'])},
                {
                    "$set": {
                        'name': form['name'],
                        'author_name': form['author_name'],
                        'book_date_added': form['book_date_added'],
                        'isbn': form['isbn'],
                        'price': form['price']
                    }
                }
            )

    test = collection.find()
    return TemplateResponse(request, 'books.html', {"books": test})


def edit_book(request):

    form = request.POST

    print form['id']

    book = collection.find_one({
        '_id':  ObjectId(form['id'])
    })

    print book['name']

    return TemplateResponse(request, 'form/edit_book.html', {"book": book})


def stats(request):  # Rendering a speficic order

    year20 = datetime.timedelta(days = -(20 *365))
    year40 = datetime.timedelta(days = -(40*365))

    vingt = (datetime.datetime.now(pytz.utc) + year20).isoformat()

    quarante = (datetime.datetime.now(pytz.utc) + year40).isoformat()

    print "20"
    print vingt
    print "40"
    print quarante

    clientaged = clientsliste.find({'birth_date': {'$gt': (quarante), '$lt': (vingt)}})



    oldestwomen = clientsliste.find({'gender': 'Female'}).sort('birth_date', pymongo.ASCENDING).limit(1)

    mailnumber = clientsliste.find()

    listemail = 0

    for mail in mailnumber:
        if '0' in str(mail["email"]) or '1' in str(mail["email"]) or '2' in str(mail["email"]) or '3' in str(mail["email"]) or '4' in str(mail["email"]) or '5' in str(mail["email"]) or '6' in str(mail["email"]) or '7' in str(mail["email"]) or '8' in str(mail["email"]) or '9' in str(mail["email"]):
            listemail = listemail +1

    return TemplateResponse(request, 'stats.html', {"mens": clientaged, "femmes": oldestwomen, "mails": listemail})