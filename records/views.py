from django.http import HttpResponse
from django.template import loader

from .models import UserProfile, Record, RecordCategory

def index(request):
    categories = RecordCategory.objects.all()
    worldRecords = []
    for category1 in categories:
        worldRecords.append(Record.objects.filter(category=category1).order_by('endurance_time')[0])
    template = loader.get_template("records/index.html")
    context = { 
            "records": worldRecords }

    return HttpResponse(template.render(context, request))


def profilePage(request, param):
    print(param)
    print("\n'n'nAAA\n\n\n")
    user1 = UserProfile.objects.all()[0]
    records = Record.objects.filter(user__username=param)

    template = loader.get_template("records/profilePage.html")
    context = { 
            "userProfile": user1, 
            "records": records }

    return HttpResponse(template.render(context, request))

def recordCategoryPage(request, propParam, propCountParam, patternParam):
    print("\n'n'nBBB\n\n\n")
    #todo validate

    category1 = RecordCategory.objects.get(prop=propParam, prop_count=int(propCountParam), pattern=patternParam)
    records = Record.objects.filter(category=category1)

    template = loader.get_template("records/recordCategoryPage.html")
    context = { 
            "category": category1, 
            "records": records }

    return HttpResponse(template.render(context, request))
