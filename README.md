#Steps to run the project

1. Create DB on Windows/Linux
2. Create virtual environment with Python 3.6
3. Install packages from `requirements.txt`
4. Run `python manage.py makemigrations`
5. Run `python manage.py migrate`
6. Run `python manage.py runserver`
7. Create a superuser with `python manage.py createsuperuser`.

### Create DB on Windows

Follow these steps to create database on Windows

    CD C:\Program Files\PostgreSQL\10\bin>psql
    psql -U postgres -h localhost
    create database socialapp;
    create user socialapp_u with password 'zYTe6sX66ebX5X8';
    grant all on database socialapp to socialapp_u;


To view the API-endpoints please visit `/docs`.

