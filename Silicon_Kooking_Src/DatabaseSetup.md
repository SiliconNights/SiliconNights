## Setting up database

#### Change database name, user, password in setting.py

#### Create database with previous name in MySQL:
```
mysql -u root -p
create database database_name;
```

#### Check and migrate with python:
```
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

#### Reset database:
```
mysql -u root -p
drop database database_name;
create database database_name;
```

Go to each app, and in the migrations folder delete everything but __init__.py file.