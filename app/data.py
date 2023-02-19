from urllib.parse import quote_plus
import pymongo
from pymongo.server_api import ServerApi
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime, timedelta

client = pymongo.MongoClient("mongodb+srv://abishekvp:" + quote_plus("Prabhason@mongodb")+ "@cluster0.x4ozo.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.chrisron
user_db = db.auth_user

for i in user_db.find_one():
    print(i)
