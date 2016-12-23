from django.http import HttpResponse
from django.template import loader

from .models import UserProfile, Record

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

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
