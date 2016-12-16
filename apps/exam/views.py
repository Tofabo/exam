from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from ..login.models import User
from .models import Item

#render's dashboard
def dashboard(request):
    if request.session['id']:
        context ={
            'user': User.objects.get(id = request.session['id']),
            'user_items': Item.objects.filter(user__id=request.session['id']),
            'other_items': Item.objects.exclude(user__id=request.session['id'])
        }
    return render(request, 'exam/dashboard.html', context)

#render's item page
def item(request, id):
    context={
        'item':Item.objects.get(id=id),
        'users': User.objects.filter(wish_items=id)
    }
    return render(request, 'exam/item.html', context)

#render's form for new item
def new_item(request):
    return render(request, 'exam/create_item.html')

#adds new item to db and redirects user to dashbaord
def create(request):
     response = Item.objects.create_item(request.POST, request.session['id'])
     if not response['status']:
            for error in response['errors']:
                messages.error(request, error)
            return redirect('exam:new_item')
     return redirect('exam:dashboard')

#deletes item from db
def delete(request,id):
    Item.objects.delete(id)
    return redirect('exam:dashboard')

#removes a  many to many relationship between a user and an item
def remove(request, id):
    Item.objects.remove(id, request.session['id'])
    return redirect('exam:dashboard')

#creates a many to many relationship between a user and an item
def add(request, id):
    Item.objects.add(id, request.session['id'])
    # user = User.objects.get(id = request.session['id'])
    # item = Item.objects.get(id=id)
    # item.user.add(user)
    return redirect('exam:dashboard')

#logs user out by clearing session and redirecting to login page
def logout(request):
    request.session.clear()
    return redirect('login:index')
