from django.http import HttpResponse
from django.template import loader
from django.core.urlresolvers import reverse 
from django.contrib.auth import authenticate, login

from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth.models import User

from .models import UserProfile, Record, RecordCategory
from .forms import RegisterForm, NewRecordForm

def newRecord(request):
    if request.method == "POST":
        form = NewRecordForm(request.POST)
        if form.is_valid():
            new_record = Record(**form.cleaned_data)
            new_record.user = request.user
            new_record.save()
            print("new record:\n\n")
            print(new_record)
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect("/records/profilePage/"+request.user.username)
    else:
        form = NewRecordForm() 

    return render(request, 'records/newRecord.html', {'form': form}) 

def registration(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("\n\n\nform:")
            print(form)
            username = form.cleaned_data["email"]
            firstname = form.cleaned_data["first_name"]
            lastname = form.cleaned_data["last_name"]
            new_user = User.objects.create_user(username,username,"changeit")
            new_user.save()
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect(reverse("index"))
    else:
        form = RegisterForm() 

    return render(request, 'registration/register.html', {'form': form}) 

def registration1(request):
    template = loader.get_template("registration/register.html")
    context = { 
            "records": None }

    return HttpResponse(template.render(context, request))


def index(request, prop="all"):
    print("\n\n\nnGET:  \n")
    print(request.GET)
    print("END GET ")
    categories = None
    if (prop == "all"):
        categories = RecordCategory.objects.all()
    else:
        categories = RecordCategory.objects.filter(prop=prop)
    worldRecords = []
    for category in categories:
        worldRecords.append(Record.objects.filter(category=category).order_by('endurance_time')[0])
    template = loader.get_template("records/index.html")
    context = { 
            "records": worldRecords,
            "props": RecordCategory.PROPS_CHOICES }

    return HttpResponse(template.render(context, request))


def profilePage(request, param):
    print(param)
    print("\n'n'nAAA\n\n\n")
    user = UserProfile.objects.all()[0]
    records = Record.objects.filter(user__username=param)

    template = loader.get_template("records/profilePage.html")
    context = { 
            "userProfile": user, 
            "records": records }

    return HttpResponse(template.render(context, request))

def recordCategoryPage(request, prop, propCount, pattern):

    print("\n\npattern:\n\n")
    print(pattern)
    #todo validate

    category = RecordCategory.objects.get(prop=prop, prop_count=int(propCount), pattern=pattern)
    records = Record.objects.filter(category=category)

    template = loader.get_template("records/recordCategoryPage.html")
    context = { 
            "category": category, 
            "records": records }

    return HttpResponse(template.render(context, request))


def loginPage(request):
    template = loader.get_template("records/base.html")
    context = {}

    return HttpResponse(template.render(context, request))
   # username = request.POST['username']
   # password = request.POST['password']
   # user = authenticate(username=username, password=password)
   # if user is not None:
   #     login(request, user)
   #     # Redirect to a success page.
   #     ...
   # else:
   #     # Return an 'invalid login' error message.
   #     ...

#The login_required decorator¶
