# algo_deep
Better algo_learning system

-------

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
