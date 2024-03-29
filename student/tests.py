# (C) 2024, PanMo LLC.
# This file is part of ConFab - DOE platform.
# Private and Confidential - donot distribute.

import os
import io
import datetime
import json
from io import BytesIO

from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.utils import timezone

from .models import Student


class StudentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.student = Student.objects.create()


    ########################## TEST CASES START #############################

    # /confab/flow/ confab.views.flow_view confab:flow_index

    def test_student_get_list_action(self):
        # Case 1: Flow search is successful, and the template is rendered
        request = self.client.get(reverse('student:listAction'))
        self.assertEqual(request.status_code, 200)
        #self.assertTemplateUsed(request, 'confab/flow_index.html')
