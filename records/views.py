from django.http import HttpResponse
from django.template import loader
from django.core.urlresolvers import reverse 
from django.contrib.auth import authenticate, login

from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth.models import User

from .models import UserProfile, Record, RecordCategory
from .forms import RegisterForm

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


def index(request):
    print("ahoj  \n\n\n")
    categories = RecordCategory.objects.all()
    worldRecords = []
    for category in categories:
        worldRecords.append(Record.objects.filter(category=category).order_by('endurance_time')[0])
    template = loader.get_template("records/index.html")
    context = { 
            "records": worldRecords }

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
    print("\n'n'nBBB\n\n\n")
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
