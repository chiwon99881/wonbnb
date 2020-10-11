# Airbnb Clone

- #1 First Init

  > Cloning Airbnb with Python

  > pip install --user pipenv

  > pipenv --three

  > pipenv shell

  > pipenv install Django==2.2.5

  > [Create Repository in github]
  > git init

  > git remote add origin [remote URL]

  > touch README.md
  > touch .gitignore

  > git add .

  > git commit -m "#1 First Init"

- #2 Create a Django Project

  > django-admin startproject config

- #3 Settings

  > linter : flake8
  > formatting : black

- #4 commander

  > python manage.py createsuperuser

  > python manage.py runserver

  > python manage.py makemigrations

  > python manage.py migrate

- #5 Application

  > django-admin startapp rooms

  > django-admin startapp users

  > django-admin startapp reviews

  > django-admin startapp conversations

  > django-admin startapp lists

  > django-admin startapp reservations

- #6 Custom User Model 1

- #7 Custom User Model 2

- #8 Custom User Model 3

- #9 Custom User Admin 1

- #10 Custom User Admin 2

- #11 Recap

- #12 TimeStampModel

- #13 Room Model 1

  > pipenv install django-countries

- #14 Room Model 2

- #15 Room Model 3

- #16 Room Model 4

- #17 Review Model

- #18 Reservation Model

- #19 List Model

- #20 Conversation Model

- #21 Refactoring Room Admin

- #22 Refactoring Room Admin 2

- #23 Refactoring Room Admin 3

- #24 QuerySet

- #25 Set related_name

- #26 Finish Room Admin

- #27 Reservation Admin

- #28 Conversations, Lists Admin

- #29 Photo uploads 1

- #30 Photo uploads 2

- #31 Photo Admin

- #32 AdminInline

- #33 super() theory

  > first, all python class have "**init**" function, this function called when the class created.
  > second, if we want override parent class method, we use overridng is right ?
  > but, if we want change parent class method, then what do you do?
  > That's super() method ! when it's used.

- #34 super().save()

- #35 create my custom commands 1

- #36 create my custom commands 2 (create amenity)

- #37 Create dummy users data by django seed

  > pipenv install django-seed

- #38 Create dummy rooms data by django seed

- #39 Create dummy photos data by django seed

  > from django.contib.admin.utils import flatten
  > flatten is simplify [[ ]] => []

- #40 Create dummy amenities,facilities,house_rules data by django seed

- #41 Create dummy reviews data by django seed

- #42 Create dummy lists data by django seed

- #43 Create dummy reservations data by django seed

- #44 Django-Template

- #45 View request

- #46 Pagination by hard coding

- #46 Pagination button by hard coding

  > Django-Template language : add

  > https://docs.djangoproject.com/en/3.1/topics/templates/#the-django-template-language

- #47 Using Django Paginator

- #48 Using Django Paginator 2

- #49 Try / Except for Handling Exception

- #50 Using ListView (Class Based View) for Paginator

- #51 Using ListView (Class Based View) for Paginator 2

- #52 Urls, Views and Arguments

- #53 get_absolute_url

- #54 Room Detail FBV

- #55 Raise 404 Page

- #56 Room Detail CBV

- #57 Search Form 1

- #58 Search Form 2

- #59 Search Form 3

- #60 Search Form 4

- #61 Search Rooms by Django Filter 1

  > https://docs.djangoproject.com/en/3.1/ref/models/querysets/#field-lookups

- #62 Search Rooms by Django Filter 2

- #63 Search Rooms by Django Forms 1

  > https://docs.djangoproject.com/en/3.1/ref/forms/api/

- #64 Search Rooms by Django Forms 2

- #65 Search Rooms by Django Forms 3

- #66 Finish Django Forms and User Login 1

- #67 User Login 2 and CSRF

- #68 User Login 3 (Validate Email)

- #69 User Login 4 (Validate Password)
