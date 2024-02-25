from urllib.request import Request
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import Student
from django.db.models import F, Model
from django.core.serializers.json import DjangoJSONEncoder
from json import dumps

from datetime import date, datetime

from django.http import JsonResponse
from django.middleware.csrf import get_token


def csrf(request):
    return JsonResponse({"csrfToken": get_token(request)})


class ModelViewBuilder:
    def __init__(self, ModelClass: Model, fields, editable, modifier={}):
        self.pk_name = ModelClass.__name__ + "Id"
        self._ModelClass = ModelClass
        self._fields = fields
        self._editable = editable
        self._modifier = modifier

    def update(self, request: Request):
        print("UPDATE ACTION")

        r = request.POST
        target = self._ModelClass.objects.filter(id=r.get(self.pk_name))

        kwargs = {name: r.get(fieldname) for name, fieldname in self._editable.items()}
        for name, modifier in self._modifier.items():
            kwargs[name] = modifier(kwargs[name])
        print(kwargs)
        target.update(**kwargs)
        data = {"Result": "OK"}
        return JsonResponse(data)

        return None

    def read(self, request: Request):
        return None

    def create(self, request: Request):
        print("CREATE ACTION")
        r = request.POST
        kwargs = {name: r.get(fieldname) for name, fieldname in self._fields.items()}
        for name, modifier in self._modifier.items():
            kwargs[name] = modifier(kwargs[name])

        s = Student.objects.create(**kwargs)

        record = kwargs
        record["id"] = s.id
        record["record_date"] = datetime.now().isoformat()[:19]

        data = {"Result": "OK", "Record": record}

        return JsonResponse(data)

    def delete(self, request: HttpRequest):
        print("DELETE ACTION")
        print(request)
        print(request.POST)

        r = request.POST
        target = self._ModelClass.objects.filter(id=r.get(self.pk_name))
        print(target)
        target.delete()

        data = {"Result": "OK"}
        return JsonResponse(data)


# Create your views here.
def listAction(request: HttpRequest):
    print("LIST ACTION")
    # '-' means descending
    print(request.POST)
    # print(students_list.order_by('-name')[:])

    s = Student.objects.values(
        StudentId=F("id"),
        Name=F("name"),
        EmailAddress=F("email_address"),
        Password=F("password"),
        Gender=F("gender"),
        BirthDate=F("birth_date"),
        Education=F("education"),
        About=F("about"),
        IsActive=F("is_active"),
        RecordDate=F("record_date"),
    )

    # wrap .values() in list because it is not serializable into JSON
    records = list(s)

    for record in records:
        if isinstance(record["BirthDate"], (date, datetime)):
            record["BirthDate"] = record["BirthDate"].isoformat()
        else:
            raise TypeError(
                "BirthDate is not a date, or datetime object and can not be converted into ISO format."
            )
        if isinstance(record["RecordDate"], (date, datetime)):
            record["RecordDate"] = record["RecordDate"].isoformat()[:19]
        else:
            raise TypeError(
                "RecordDate is not a date, or datetime object and can not be converted into ISO format."
            )

    # sorting by field:
    sort_field = request.GET["jtSorting"]
    field, direction = sort_field.split(" ")
    reverse = direction.upper() == "DESC"
    records = sorted(records, key=lambda rec: rec[field], reverse=reverse)

    # list(s) -> "Records"
    data = {"Result": "OK", "Records": records}

    return JsonResponse(data, safe=False)
    # safe=False means types other than dict can be sent


studentCRUD = ModelViewBuilder(
    Student,
    {
        "name": "Name",
        "email_address": "EmailAddress",
        "password": "Password",
        "gender": "Gender",
        "birth_date": "BirthDate",
        "education": "Education",
        "about": "About",
        "is_active": "IsActive",
    },
    {
        "name": "Name",
        "email_address": "EmailAddress",
        "password": "Password",
        "gender": "Gender",
        "education": "Education",
        "about": "About",
        "is_active": "IsActive",
    },
    modifier={"is_active": bool},
)


def updateAction(request: HttpRequest):
    return studentCRUD.update(request)


def createAction(request: HttpRequest):
    return studentCRUD.create(request)


def deleteAction(request: HttpRequest):
    return studentCRUD.delete(request)
