from django.http import HttpResponse
from django.template import loader

from django.contrib.auth import authenticate, login

from .models import UserProfile, Record, RecordCategory

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
