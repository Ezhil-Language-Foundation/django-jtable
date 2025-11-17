from django.http import HttpRequest

from student.models import Student

from django.http import JsonResponse
from django.middleware.csrf import get_token

from django_jtable.viewbuilder import ModelViewBuilder


def csrf(request):
    return JsonResponse({"csrfToken": get_token(request)})


studentCRUD = ModelViewBuilder(
    Student,
    {
        "id": "StudentId",
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
    datefields=[
        "BirthDate",
    ],
)


# Create your views here.
def listAction(request: HttpRequest):
    return studentCRUD.read(request)


def updateAction(request: HttpRequest):
    return studentCRUD.update(request)


def createAction(request: HttpRequest):
    return studentCRUD.create(request)


def deleteAction(request: HttpRequest):
    return studentCRUD.delete(request)
