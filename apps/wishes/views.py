# coding: utf-8
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Wish

# Create your views here.
def index(request):
    return render(request, "wishes/index.html")

def login(request):
    if request.method == "POST":
        user = User.objects.login(request.POST)
        if not user:
            messages.error(request, "Invalid login credentials!")
        else:
            request.session['logged_user'] = user.id
            return redirect('/dashboard')
    return redirect('/')


def register(request):
    if request.method == "POST":
        form_errors = User.objects.validate_user_info(request.POST)
        if len(form_errors) > 0:
            for error in form_errors:
                messages.error(request, error)
        else:
            User.objects.register(request.POST)
            messages.success(request, "You have Successfully registered! Please sign-in to continue")

    return redirect('/')

def dashboard(request):
    if "logged_user" not in request.session:
        messages.error(request, "You need to login to see that")
        return redirect('/')
    user = User.objects.get(id=request.session['logged_user'])
    all_wishes = Wish.objects.filter(users=user) | Wish.objects.filter(user_wish=user)
    context = {
        'user' : User.objects.get(id=request.session['logged_user']),
        'my_wishes' : all_wishes,
        'other_wishes': Wish.objects.exclude(id__in=all_wishes)
    }
    return render(request, 'wishes/dashboard.html', context)

def add(request):
    if "logged_user" not in request.session:
        messages.error(request, "Gotta login bro")
        return redirect('/')
    return render(request, 'wishes/create.html')

def add_wish(request):
    if "logged_user" not in request.session:
        messages.error(request, "Gotta login bro")
        return redirect('/')
    if request.method == "POST":
        errors = Wish.objects.check_form_data(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect("/add")
        else:
            user = User.objects.get(id=request.session['logged_user'])
            wish= Wish.objects.create(item=request.POST['item'], user_wish=user)
    return redirect('/dashboard', wish_id=wish.id)

def join(request, id):
    wish = Wish.objects.get(id=id)
    user = User.objects.get(id=request.session['logged_user'])
    wish.users.add(user)
    wish.save()
    return redirect('/dashboard')



def wish_items(request, id):
    if "logged_user" not in request.session:
        messages.error(request, "Gotta login bro")
        return redirect('/')
    wish = Wish.objects.get(id=id)
    users = User.objects.all()
    joined = User.objects.filter(wishes=wish)
    context = {
        'wish':wish,
        'users': users,
        'joined': joined
    }
    return render(request, "wishes/item.html", context)

def remove(request, wish_id):
    wish= Wish.objects.get(id=wish_id)
    user = User.objects.get(id=request.session['logged_user'])
    wish.users.remove(user)
    return redirect('/dashboard')


def delete(request, wish_id):
    wish = Wish.objects.get(id=wish_id)
    wish.delete()
    return redirect('/dashboard')

def logout(request):
    if "logged_user" in request.session:
        #remove the logged in user from the session
        request.session.pop('logged_user')
        #redirect to the index page
    return redirect('/')
