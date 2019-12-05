A simple social application based on Django.

![Login Page](https://i.imgur.com/9Muw11n.jpg)


# Steps to run the project

1. Create a database in Postgres
2. Create virtual environment with Python 3.6
3. Install packages from `requirements.txt`
4. Create an `.env` file. (a sample is at the end of readme)
4. Run `python manage.py makemigrations`
5. Run `python manage.py migrate`
6. Run `python manage.py collectstatic`
7. Run `python manage.py runserver`
8. Create a superuser with `python manage.py createsuperuser`.

### Create DB on Windows


Follow these steps to create database on Windows

    CD C:\Program Files\PostgreSQL\10\bin>psql
    psql -U postgres -h localhost
    create database socialapp;
    create user socialapp_u with password 'zYTe6sX66ebX5X8';
    grant all on database socialapp to socialapp_u;

Where `zYTe6sX66ebX5X8` is the user password, set it to your preference.


If you use Linux

    sudo -u postgres createuser -S -D -R -P socialapp_u
    sudo -u postgres createdb -O socialapp_u socialapp -E utf-8

On first command it asks for user's password set it to your preference.


### Environment File 

The following is `.env` sample.
    
    SECRET_KEY=YOUR_KEY
    DEBUG=False
    DB_NAME=socialapp
    DB_USER=socialapp_u
    DB_PASSWORD=zYTe6sX66ebX5X8

Generate a random secret key by:

    from django.core.management.utils import get_random_secret_key
    get_random_secret_key()

Modify the sample file `SECRET_KEY` with the output. Replace `DB_PASSWORD` with password you have set.


### API Endpoints

To view the API-endpoints please visit `/docs`.


### Improvements

1. Add static types, improve readability. 
2. Automate deployment, use Docker. 
3. Use CropperJS for image uploading.
4. Add notifications via `messages.framework`


