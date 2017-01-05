"""Controller methods"""
from django.http import HttpResponse
from django.template import loader
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth.models import User

from .models import UserProfile, Record, RecordCategory
from .forms import RegisterForm, NewRecordForm

def new_entry(request):
    if request.method == "POST":
        form = NewRecordForm(request.POST)
        handle_new_entry_form(request, form)
    else:
        form = NewRecordForm()

    return render(request, 'records/newRecord.html', {'form': form})

def handle_new_entry_form(request, form):
    if form.is_valid():
        new_record = Record(**form.cleaned_data)
        new_record.user = request.user
        new_record.save()
        return HttpResponseRedirect("/records/profilePage/"+request.user.username)

def registration(request):
    """ not sure how to divide this method into shorter ones """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["email"]
            new_user = User.objects.create_user(username, username, "changeit")
            new_user.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def registration1(request):
    template = loader.get_template("registration/register.html")
    context = {"records": None}

    return HttpResponse(template.render(context, request))


def index(request, prop="all"):
    world_records = handle_filters(prop)
    template = loader.get_template("records/index.html")
    context = {"records": world_records, "props": RecordCategory.PROPS_CHOICES}

    return HttpResponse(template.render(context, request))

def handle_filters(prop):
    """"returns list of world_records for index page based on various filters on page"""
    world_records = []
    categories = []
    if prop == "all":
        categories = RecordCategory.objects.all()
    else:
        categories = RecordCategory.objects.filter(prop=prop)
    for category in categories:
        world_records.append(Record.objects.filter(category=category).order_by('endurance_time')[0])
    return world_records

def profile_page(request, param):
    user = UserProfile.objects.all()[0]
    records = Record.objects.filter(user__username=param)

    template = loader.get_template("records/profilePage.html")
    context = {"userProfile": user, "records": records}

    return HttpResponse(template.render(context, request))

def record_category_page(request, prop, prop_count, pattern):
    category = RecordCategory.objects.get(prop=prop, prop_count=int(prop_count), pattern=pattern)
    records = Record.objects.filter(category=category)

    template = loader.get_template("records/recordCategoryPage.html")
    context = {"category": category, "records": records}

    return HttpResponse(template.render(context, request))


def login_page(request):
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

def account_settings(request):
    return render(request, 'records/accountSettings.html', None)

#The login_required decorator¶
