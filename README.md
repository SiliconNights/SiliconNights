## SCRUM Meetings
#### [Scrum Meetings](https://docs.google.com/spreadsheets/d/1V9OtsbMmw0wnypaUizGiNEG1rD8Z_nNtrYLTDAiGpLY/edit?usp=sharing)


## Set Up Local Git and Clone Repository

*Commands run on Windows PowerShell*

[Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)


#### Set Up Git Info

[Github: Set up Git](https://help.github.com/articles/set-up-git/#next-steps-authenticating-with-github-from-git)

#### Fork repository and clone to desktop

[Github: Fork a Repo](https://help.github.com/articles/fork-a-repo/)

#### List branches

```
git branch
```

#### Checkout a branch

```
git checkout branch_name
```
[Basic Branching and Merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)

#### Staging and Committing 

[Saving Changes](https://www.atlassian.com/git/tutorials/saving-changes)

#### Check status 
```
git status
```
#### Ignoring files
[.gitignore](https://www.atlassian.com/git/tutorials/gitignore)

## Set Up Development Stack

### Install Python
Version: *Python 3.6.4*

[Python download](https://www.python.org/downloads/)

### Install Virtual Environment (Optional: dedicated environment)
[virtualenv pip install](https://docs.djangoproject.com/en/2.0/howto/windows/)

### Install Django
Version: *Django 2.0*
```
pip install Django==2.0
```
### Set up MySQL

#### Install MySQL
*Record root password!*

[Download MySQL Community Server 5.7.21](https://dev.mysql.com/downloads/mysql/)

#### Add MySQL to PATH
[Add bin to PATH](https://dev.mysql.com/doc/mysql-windows-excerpt/5.7/en/mysql-installation-windows-path.html)

#### Check installation 
```
mysql --version
mysql -u root -p
\q
```


## Start New Project

#### Create project
Navigate to working directory (git repository)
```
django-admin startproject name
```

#### Run Server 
```
cd /name
python manage.py runserver
```
Go to URL


## Connect Django to MySQL

#### Create Database in MySQL
```
mysql -u root -p
sql> create database my_db;
sql> show databases;
sql> \q
```

#### Install MySQL API  

```
pip install mysqlclient
```


#### Edit setting.py

```python
DATABASES = {
    'default': {
        'NAME': 'my_db',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'rootpassword',      
    }
}
```

[Stackoverflow reference](https://stackoverflow.com/questions/22419210/django-and-mysql-problems-on-mavericks)

#### Check and run
```
python manage.py check
python manage.py migrate auth
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Editing README.md
[Markdown Cheat sheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

