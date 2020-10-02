# Airbnb Clone

- #1 First Init

Cloning Airbnb with Python

pip install --user pipenv

pipenv --three

pipenv shell

pipenv install Django==2.2.5

[Create Repository in github]
git init

git remote add origin [remote URL]

touch README.md
touch .gitignore

git add .

git commit -m "#1 First Init"

- #2 Create a Django Project

django-admin startproject config

- #3 Settings

linter : flake8
formatting : black

- #4 commander

python manage.py createsuperuser

python manage.py runserver

python manage.py migrate

- #5 Application

django-admin startapp rooms
django-admin startapp users
django-admin startapp reviews
django-admin startapp conversations
django-admin startapp lists
django-admin startapp reservations

- #6 Custom User Model 1

- #7 Custom User Model 2

- #8 Custom User Model 3

- #9 Custom User Admin 1

- #10 Custom User Admin 2

- #11 Recap

- #12 TimeStampModel

- #13 Room Model 1

pipenv install django-countries

- #14 Room Model 2

- #15 Room Model 3

- #16 Room Model 4
