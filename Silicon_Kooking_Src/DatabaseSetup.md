## Setting up database

#### Change database name, user, password in setting.py and add:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name',
        'USER': 'root',
        'PASSWORD': 'rootpassword',
		'OPTIONS': {
         "init_command": "SET foreign_key_checks = 0;",
		},
    }
}
```

#### Create database with previous name in MySQL:
```
mysql -u root -p
create database database_name character set utf8 collate utf8_unicode_ci;
```

#### Check and migrate with python:
```
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Populate recipes table 

#### Data
 Uncompress inputdata.7z

#### Set limit
To set number of recipes to add to database, modify last-recipe.txt [max = 793].

#### Run in sequence

```
python manage.py populate ing
python manage.py populate rec
```

## Reset database:
```
mysql -u root -p
drop database database_name;
create database database_name character set utf8 collate utf8_unicode_ci;
```

Go to each app, and in the migrations folder delete everything but ```__init__.py``` file.
