from urllib.request import Request
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import Student
from django.db.models import F
from django.core.serializers.json import DjangoJSONEncoder
from json import dumps

from datetime import date, datetime

from django.http import JsonResponse
from django.middleware.csrf import get_token

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

# Create your views here.
# TODO: Add CSRF protection after creating log in functionality.
def listAction(request: HttpRequest):
    print('LIST ACTION')
    # '-' means descending
    print(request.POST)
    # print(students_list.order_by('-name')[:])

    s = Student.objects.values(
        StudentId=F('id'),
        Name=F('name'),
        EmailAddress=F('email_address'),
        Password=F('password'),
        Gender=F('gender'),
        BirthDate=F('birth_date'),
        Education=F('education'),
        About=F('about'),
        IsActive=F('is_active'),
        RecordDate=F('record_date'),
    )

    # wrap .values() in list because it is not serializable into JSON
    records = list(s)

    for record in records:
        if isinstance(record['BirthDate'], (date, datetime)):
            record['BirthDate'] = record['BirthDate'].isoformat()
        else:
            raise TypeError('BirthDate is not a date, or datetime object and can not be converted into ISO format.')
        if isinstance(record['RecordDate'], (date, datetime)):
            record['RecordDate'] = record['RecordDate'].isoformat()[:19]
        else:
            raise TypeError('RecordDate is not a date, or datetime object and can not be converted into ISO format.')

    # sorting by field:
    sort_field = request.GET['jtSorting']
    field,direction = sort_field.split(' ')
    reverse =  (direction.upper() == 'DESC')
    records = sorted(records,key=lambda rec: rec[field] ,reverse=reverse)

    # list(s) -> "Records"
    data = {
        "Result": "OK",
        "Records": records
    }

    return JsonResponse(data, safe=False)
    # safe=False means types other than dict can be sent

def updateAction(request: HttpRequest):
    print('UPDATE ACTION')

    r = request.POST

    target = Student.objects.filter(id=r.get('StudentId'))
    target.update(
        name=r.get('Name'),
        email_address=r.get('EmailAddress'),
        password=r.get('Password'),
        gender=r.get('Gender'),
        birth_date=r.get('BirthDate'),
        education=r.get('Education'),
        about=r.get('About'),
        is_active=bool(r.get('IsActive'))
    )

    data = {
        "Result":"OK"
    }

    return JsonResponse(data)

def createAction(request: HttpRequest):
    print('CREATE ACTION')
    r = request.POST
    print(request.POST)
    values = [
        'Name',
        'EmailAddress',
        'Password',
        'Gender',
        'BirthDate',
        'Education',
        'About',
        'IsActive'
    ]

    s = Student.objects.create(
        name=r['Name'],
        email_address=r['EmailAddress'],
        password=r['Password'],
        gender=r['Gender'],
        birth_date=r['BirthDate'],
        education=r['Education'],
        about=r['About'],
        is_active=bool(r['IsActive'])
    )

    record = {}
    for value in values:
        record[value] = r.get(value)

    record['id'] = s.id
    record['record_date'] = datetime.now().isoformat()[:19]

    data = {
        "Result": "OK",
        "Record": record
    }

    return JsonResponse(data)

def deleteAction(request: HttpRequest):
    print('DELETE ACTION')
    print(request)
    print(request.POST)

    r = request.POST
    target = Student.objects.filter(id=r.get('StudentId'))
    print(target)
    target.delete()

    data = {
        "Result": "OK"
    }

    return JsonResponse(data)
