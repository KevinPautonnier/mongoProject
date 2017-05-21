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

    client20to40 = clientsliste.find(
        {'birth_date':{'$gt': (vingt), '$lt': (quarante)}}
    )



    # Femme la plus agée

    oldestwomen = clientsliste.find( {'gender' : 'Female', }).sort({ "birth_date" : 1 }).limit(1)




    return TemplateResponse(request, 'stats.html', {"clients": client20to40}, {"oldest" : oldestwomen})
