## AlgoLearn
Algolearn.  What is it?
 If you are a student, teacher, or just a person who wants to understand the algorithms, their structure, to know why they are needed, then you should know about our project.
 We are the Algolearn team, which has made a learning platform for you on algorithms, where you can become a student or teacher, receive or transfer your knowledge.
 How it works?
 You register, choose a course, get marks for passing it, test your knowledge during tests.
 The teacher can create his course and start to supervise the “class”, a group of people who have chosen your course.
 That's it, a brief excursion into our world of algorithms.
 Thank you for your attention.
----
#### python3.7

## to create and activate venv
```bash
python3 -m venv venv
source venv/bin/activate
```

## to create requirements.txt
```bash
pip freeze > requirements.txt
```

## to install everything from requirements.txt
```bash
pip install -r requirements.txt
```

------------------------------

### **I am not sharing database now. Create your own one. All this information will be hidden.**


## to install postgre
```bash
sudo apt-get install postgresql postgresql-server-dev
```

## to check version
```bash
psql -V
```

## start configuring database and user
```bash
create user gda2048 with password 'algolearn';
alter role gda2048 set client_encoding to 'utf8';
alter role gda2048 set default_transaction_isolation to 'read committed';
alter role gda2048 set timezone to 'UTC';
create database algo_learn_psql owner gda2048;
```

### database PostgreSQL 10.7
```python3
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'algo_learn_psql',
    'USER': 'gda2048',
    'PASSWORD': 'algolearn',
    'HOST': '127.0.0.1',
    'PORT': '5432',
```

--------

## Create first user (superuser) 
for using admin panel _.../admin/_
```bash
python3.7 manage.py createsuperuser
```
```python3
    'Username': 'gda2048'
    'email': 'goncharovdma@gmail.com'
    'password': 'algolearn'
```
### Heroku
_in algo_deep repo:_
```bash
heroku login
heroku git:remote algo2048demo
git push heroku dev:master # pushing

```
