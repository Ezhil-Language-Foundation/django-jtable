from django.db import models

from datetime import date

# Create your models here.


class Student(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)

    email_address = models.EmailField(max_length=200)

    password = models.CharField(max_length=200)

    class GenderChoices(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
    )

    birth_date = models.DateField()

    class EducationChoices(models.TextChoices):
        PRIMARY = "1", "Primary school"
        HIGH_SCHOOL = "2", "High school"
        UNIVERSITY = "3", "University"

    education = models.CharField(
        max_length=1,
        choices=EducationChoices.choices,
    )

    about = models.TextField()

    is_active = models.BooleanField()

    # auto_now_add sets the DateTimeField to the datetime of when the object is created.
    record_date = models.DateTimeField(auto_now_add=True)
