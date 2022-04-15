# API_USERS
This is a little API for USERS data

# first of all u need to pull git by command: git pull https://github.com/Owenzbs/API_USERS.git

  - You need to install all requirments by command: pip install -r requirements.txt

You need to make changes in settings.py

  - change the database info to connect to your database
  - change the parametrs for email
You need to apply this commands to make mirgrations:

  - python manage.py makemigrations
  - python manage.pt migrate
If all fine then u can run server and check working API: python manage.pt runserver

and then u can check it by Postman or REST Framework

- urls:
  - /api/users POST
  - /api/login POST
  - /api/users/id POST
  - /api/users/id GET
