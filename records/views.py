"""Controller methods"""
from django.http import HttpResponse
from django.template import loader
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import UserProfile, Record, RecordCategory
from .forms import RegisterForm, NewRecordForm, UserProfileForm, UserSimpleForm

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
    """ handling registration """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["email"]
            default_password = "changeit"
            new_user = User.objects.create_user(username, username, default_password)
            new_user.save()

            new_user = authenticate(username=username, password=default_password)
            login(request, new_user)

            UserProfile.objects.create(user=new_user)

            return HttpResponseRedirect(reverse("index"))
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


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
        records = Record.objects.filter(category=category).order_by('endurance_time')
        if records != None:
            world_records.append(records[0])
    return world_records

def profile_page(request, param):
    user = UserProfile.objects.get(user__username=param)
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

def account_settings(request):
    return handle_edit_user_form(request)

def handle_edit_user_form(request):
    """ not sure how to divide this method into shorter ones """
    current_user = User.objects.get(username=request.user)
    current_userprofile = current_user.userprofile
    if request.method == "POST":
        user_simple_form = UserSimpleForm(request.POST, instance=current_user)
        user_profile_form = UserProfileForm(request.POST, instance=current_userprofile)
        if user_simple_form.is_valid():
            user_simple_form.save()

        if user_profile_form.is_valid():
            user_profile_form.save()
    else:
        user_simple_form = UserSimpleForm(instance=current_user)
        user_profile_form = UserProfileForm(instance=current_userprofile)

    forms = {'user_simple_form': user_simple_form, 'user_profile_form': user_profile_form}
    return render(request, 'records/accountSettings.html', forms)
#The login_required decorator¶
