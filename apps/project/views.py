# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import User, Quote
from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return render(request, 'project/login.html')

def register(request):
    data = {
    "username": request.POST['username'],
    'first_name': request.POST['first_name'],
    'last_name': request.POST['last_name'],
    'email': request.POST['email'],
    'password': request.POST['password'],
    'confirm_pw': request.POST['confirm_pw']
    }
    warnings=User.objects.validate(data)
    if not warnings:
        request.session['current_user_id'] = User.objects.create(username=data['username'],first_name=data['first_name'],last_name=data['last_name'], email=data['email'],password=User.objects.hashPW(data)).id
        return redirect('/quotes')
    else:
        for i in warnings:
            messages.error(request, i)
        return redirect('/')
    pass

def login(request):
    data = {
    'username': request.POST['username'],
    'password': request.POST['password']
    }
    warnings=User.objects.login(data)
    if not warnings:
        request.session['current_user_id'] = User.objects.get(username=data['username']).id
        return redirect('/quotes')
    else:
        for i in warnings:
            messages.error(request,i)
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def quotes(request):
    context= {
    'quotes': Quote.objects.all(),
    'user': User.objects.get(id=request.session['current_user_id']),
    'favorites': User.objects.get(id=request.session['current_user_id']).users.all()
    }
    return render(request, 'project/quotes.html', context)

def submitquote(request):
    data = {
    'author': request.POST['author'],
    'quote': request.POST['quote'],
    'user': User.objects.get(id=request.session['current_user_id'])
    }
    warnings= Quote.objects.validate(data)
    if not warnings:
        Quote.objects.create(author=data['author'],content=data['quote'],user=data['user'])
        return redirect('/quotes')
    else:
        for i in warnings:
            messages.error(request, i)
        return redirect('/quotes')

def addfavorite(request, id):
    user = User.objects.get(id=request.session['current_user_id'])
    quote = Quote.objects.get(id=id)
    quote.favorites.add(user)
    return redirect('/quotes')

def removefavorite(request, id):
        user = User.objects.get(id=request.session['current_user_id'])
        quote = Quote.objects.get(id=id)
        quote.favorites.remove(user)
        return redirect('/quotes')

def users(request, id):
    user= User.objects.get(id=id)
    context = {
    'user': user,
    'quotes': Quote.objects.filter(user=user)
    }
    return render(request, 'project/user.html', context)
