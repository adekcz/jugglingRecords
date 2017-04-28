"""Controller methods"""
from django.http import HttpResponse
from django.template import loader
from django.core.urlresolvers import reverse, reverse_lazy

from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.views.generic import DeleteView
from django.core.exceptions import PermissionDenied

from .models import UserProfile, Record, RecordCategory
from .forms import RegisterForm, NewRecordForm, UserProfileForm
from .forms import UserSimpleForm, RecordsFilterForm, NewRecordCategoryForm


class PermissionMixin(object):

    def get_object(self, *args, **kwargs):
        obj = super(PermissionMixin, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user:
            raise PermissionDenied()
        else:
            return obj

def new_entry(request, category_id=None):
    if request.method == "POST":
        form = NewRecordForm(request.POST)
        response = handle_new_entry_form(request, form)
        if response != None:
            return response
    else:
        if category_id != None:
            category = RecordCategory.objects.get(pk=category_id)
            record = Record()
            record.category = category
            form = NewRecordForm(instance=record)
        else:
            form = NewRecordForm()

    return render(request, 'records/newRecord.html', {'form': form})

def edit_entry(request, key):
    """ lalala """
    record = Record.objects.get(pk=key)
    if request.method == "POST":
        form = NewRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
    else:
        form = NewRecordForm(instance=record)

    return render(request, 'records/newRecord.html', {'form': form})

def handle_new_entry_form(request, form):
    if form.is_valid():
        new_record = Record(**form.cleaned_data)
        new_record.user = request.user
        new_record.save()
        return HttpResponseRedirect("/records/profilePage/"+request.user.username)

def new_category(request):
    if request.method == "POST":
        form = NewRecordCategoryForm(request.POST)
        response = handle_new_category_form(form)
        if response != None:
            return response
    else:
        form = NewRecordCategoryForm()

    return render(request, 'records/newCategory.html', {'form': form})

def handle_new_category_form(form):
    if form.is_valid():
        created_category = RecordCategory(**form.cleaned_data)
        created_category.save()
        print("should redirect to:")
        print("/records/newRecord/"+str(created_category.id))
        return HttpResponseRedirect("/records/newRecord/"+str(created_category.id))

def registration(request):
    """ handling registration """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            new_user = User.objects.create_user(username, username, password)
            new_user.save()

            new_user = authenticate(username=username, password=password)
            login(request, new_user)

            UserProfile.objects.create(user=new_user)

            return HttpResponseRedirect(reverse("index"))
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def index(request):
    """ lalala """
    world_records = None
    prop = "ALL_PROPS"
    record_type = "ALL_TYPES"
    if request.method == "POST":
        form = RecordsFilterForm(request.POST)
        if form.is_valid():
            print("\n\n\nAAAA")
            print(form)
            prop = form.cleaned_data['prop']
            record_type = form.cleaned_data['record_type']
            print(prop)
            print(record_type)
            world_records = handle_filters(prop, record_type)

    if world_records is None:
        form = RecordsFilterForm()
        world_records = handle_filters()

    template = loader.get_template("records/index.html")
    context = {"records": world_records, "props": RecordCategory.PROPS_CHOICES,
               "types": RecordCategory.RECORD_TYPE_CHOICES, "form":form,
               "selected_prop":prop, "selected_record_type":record_type}

    print("\ncontext:")
    print(context)
    print("testingWhatWasSelected")
    print()
    return HttpResponse(template.render(context, request))

#todo change hardcoded mess for values
def handle_filters(prop="ALL_PROPS", record_type="ALL_TYPES"):
    """"returns list of world_records for index page based on various filters on page"""
    world_records = []
    categories = []
    #TODO this is ugly
    if prop == "ALL_PROPS" and record_type == "ALL_TYPES":
        categories = RecordCategory.objects.all()
    elif prop == "ALL_PROPS":
        categories = RecordCategory.objects.filter(record_type=record_type)
    elif record_type == "ALL_TYPES":
        categories = RecordCategory.objects.filter(prop=prop)
    else:
        categories = RecordCategory.objects.filter(prop=prop).filter(record_type=record_type)
    for category in categories:
        records = Record.objects.filter(category=category).order_by('endurance_time')
        if records != None and len(records) > 0:
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

class RecordDelete(PermissionMixin, DeleteView):
    model = Record
    success_url = reverse_lazy('accountSettings')
