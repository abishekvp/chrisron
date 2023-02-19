from urllib.parse import quote_plus
import pymongo
from pymongo.server_api import ServerApi
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime, timedelta

client = pymongo.MongoClient("mongodb+srv://abishekvp:" + quote_plus("Prabhason@mongodb")+ "@cluster0.x4ozo.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.chrisron
user_db = db.users
auth_user = db.auth_user

month = ["",'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

from django import template

register = template.Library()

@register.filter
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


def index(request):
    return render(request,'index.html')

def main(request):
    try:
        u_name = request.user.username
        if request.method == 'POST':
            value = request.POST["submit"]
            print(value)
            if value=="claim":
                user_info = user_db.find_one({'wallet_address':u_name})
                now = datetime.now()
                time = now + timedelta(minutes = 30)
                time = int(time.timestamp() * 1000)                       
                user_info['timer'] = time
                user_info['claim'] = int(user_info['claim']+1)        
                user_db.find_one_and_update(filter={'wallet_address':u_name},update={'$set':user_info})
                return redirect("index")
            
            elif value=="withdrawl":
                user_info = user_db.find_one({'wallet_address':u_name})
                if user_info['claim']>=250:
                    user_info['withdrawl'] = user_info['withdrawl']+user_info['claim']
                    user_info['claim']=0
                    now = datetime.now()
                    time = now + timedelta(minutes = 30)
                    time = int(time.timestamp() * 1000)        
                    user_info['timer'] = time
                    user_db.find_one_and_update(filter={'wallet_address':u_name},update={'$set':user_info})
                else:
                    messages.success(request, 'Claim 250 tokens to withdrawl')
                return redirect("index")
        
        user_info = user_db.find_one({'wallet_address':u_name})
        request.session['timer']=user_info['timer']
        request.session['claim']=user_info['claim']
        request.session['withdrawl']=user_info['withdrawl']
        return render(request,'main.html',{'timer':request.session.get('timer'),'claim':request.session.get('claim'),'withdrawl':request.session.get('withdrawl')})
    except:return HttpResponse("<center><h1>Something went Wrong</h1></center>")


def user_register(request):
    if request.method == 'POST':
        wallet_address = request.POST["wallet_address"]
        passcode = request.POST["password"]
        now = datetime.now()
        time = now + timedelta(minutes = 30, seconds = 20)
        time = int(time.timestamp() * 1000)
        User.objects.create_user(username = wallet_address, password = passcode)
        user_db.insert_one({'wallet_address':wallet_address, 'password':passcode, 'claim':0, 'withdrawl':0, 'timer':time})
        user = authenticate(request, username=wallet_address, password=passcode)

        if user is not None:
            login(request=request, user=user)
            return redirect('index')
        else:
            messages.success(request, 'user not found')

    return render(request,'./registration/register.html')

def user_login(request):
    if request.method == 'POST':
        wallet_address = request.POST["wallet_address"]
        passcode = request.POST["password"]
        print(wallet_address,passcode)
        
        user = authenticate(request, username=wallet_address, password=passcode)

        if user is not None:
            login(request=request,user=user)
            return redirect('index')
        else:
            messages.success(request, 'user not found')
        

    return render(request,'./registration/login.html')
    

def show(request):
    dic = list(user_db.find())
    out_dic={}
    for i in dic:
        dic_v = {'claim':i['claim'],'withdrawl':i['withdrawl']}
        out_dic[i["wallet_address"]] = dic_v
    print(out_dic)

    return render(request,"view.html",{'data_dic':out_dic})

def user_logout(request):
    logout(request)
    return redirect('login')