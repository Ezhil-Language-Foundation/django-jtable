Instructions to start the Django server
1. You should now be running the virtual environment from the project's root folder.
2. Run the command "python3 manage.py migrate --run-syncdb" (if this did not work you can also try,
   "python3 manage.py migrate --run-syncdb")
3. You should see something like,


![Example Use](static/assets/edit_example.png)

```	
Operations to perform:
  Synchronize unmigrated apps: corsheaders, messages, staticfiles, tables
  Apply all migrations: admin, auth, contenttypes, sessions
Synchronizing apps without migrations:
  Creating tables...
    Creating table tables_student
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
```
4. Run the command "python manage.py runserver" in order to run the Django server.

Now, the server should be up and running and should be accessible from "http://127.0.0.1:8000/"
You should see something like this screenshot with a "The Student List" displayed. You should be
able to perform CRUD operations on the student table sufficiently easily.

The currently accessible links are:
   1. "http://127.0.0.1:8000/action/listAction" gets the data from the backend to display in the jTable.
   2. "http://127.0.0.1:8000/action/createAction" sends data from the jTable to the backend to create a new record.
   3. "http://127.0.0.1:8000/action/deleteAction" sends the id of the record to delete from the backend.
   4. "http://127.0.0.1:8000/action/updateAction" send the data from the jTable to the backend to update an existing record.

5. To setup admin access to the site, use the command "python3 manage.py createsuperuser" and setup username and password.
   Launch the server and navigate to the admin page at URL "http://127.0.0.1:8000/admin/" login with the credential and update
   the database tables / add / delete entries etc.


6. LICENSE
   - the Django JTable project is licensed under the MIT License as well like the JTable widget.
   - the original JTable widget is distributed in this package but not part of this project
     jTable is developed by Halil İbrahim Kalkan and licensed under MIT License. See: https://www.jtable.org/Home/About

7. Works with jTable 2.4.0; please download and install this package; it is not distributed with the pypi package.

Notes
-----
- Created: 8/3/2022
- Last updated: 11/17/2025
