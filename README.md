
# **Popflix**

This is a Django REST based media manager designed with an adaptive & hierarchical file structure. Popflix would function as an ideal API back-end for any media manager project whether the key file type was audio, video, text etc, etc. There is a full choice of bonus features including a testing suite, advanced filtering, containerization and CI/CD prebuilt.


## Features

**API**
- Adaptive API allowing completely arbitrary depth of channels/objects.

**Channel rating Utility**
- Depth-first search algorithm to trace all nodes (channel's ratings), summing them on each branch (superchannel) backtracking to root (origin channel).

**Filtering**
- Category (Groups) options available to each channel/superchannel that can be easily query filtered. 

**Testing suite**
- Unit testing that covers all project's features with a test coverage of over 93%.


## Technologies

- [VS Code](https://code.visualstudio.com//) - Used as core IDE.
- [GitHub](https://github.com/) - Used as remote storage.

- **Python**    
    - [Python 3.11.0](https://www.python.org/) - Used as base programming language.
- **Django**
    - [Django 4.2.8](https://www.djangoproject.com/) - As python web framework for rapid development.
    - [Django REST 3.14.0](https://www.django-rest-framework.org/) - Django-based toolkit for building Web APIs.
- **Database**
    - [SQlite3](https://www.sqlite.org/index.html) - For a development database, provided by Django.
- **Docker**
    - [Docker](https://www.docker.com/) - Platform designed to help build, share, and run container applications.
- **Testing**    
    - [Coverage 7.4.1](https://pypi.org/project/coverage/) - Code coverage measurement for Python.
- **CI/CD**
    - [GitHub Actions](https://github.com/features/actions) - Build, test, and deploy from your remote storage.
\


## Database Design:

- [SQlite3](https://www.sqlite.org/index.html) - For development database, provided by Django.

### Data Models:

**Users**

The User model utilized for this project is the standard one provided by **`django.contrib.auth.models`**

\
**Group model**

| Name | Key in db | Validation | Field Type |
--- | --- | --- | ---
Title | title | max_length=250 | CharField
Active | active | default=True, null=True | BooleanField
Picture Url | picture_url | max_length=250, null=True, blank=True | URLField
Slug | slug | max_length=250, unique=True, null=True, blank=True | SlugField

\
**Channel model**

| Name | Key in db | Validation | Field Type |
--- | --- | --- | ---
Title | title | max_length=250 | CharField
Language | Language | max_length=250 | CharField
Active | active | default=True, null=True | BooleanField
Picture Url | picture_url | max_length=250, null=True, blank=True | URLField
Groups | groups | blank=True | ManyToManyField
Slug | slug | max_length=250, unique=True, null=True, blank=True | SlugField
Superchannel | superchannel | on_delete=models.SET_NULL, null=True, blank=True | ForeignKey

\
**Content model**

| Name | Key in db | Validation | Field Type |
--- | --- | --- | ---
Name | name | max_length=250 | CharField
Description | description | max_length=2500 | TextField
Genre | genre | max_length=250 | CharField
Authors | authors | max_length=250 | CharField
File Url | file_url | max_length=250 | URLField
Active | active | default=True, null=True | BooleanField
Slug | slug | max_length=250, unique=True, null=True, blank=True | SlugField
Rating | rating | MinValueValidator(0), MaxValueValidator(10) | DecimalField
Channel | channel | on_delete=models.SET_NULL, null=True, blank=True | ForeignKey


## Deployment

### Local Deployment 

Please note - in order to run this project locally on your own system, you will need the following installed:
- [Python3](https://www.python.org/) to run the application.
- [PIP](https://pip.pypa.io/en/stable/) to install app requirements.
- [GIT](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) for version control.

1. Clone the Popflix repository by either downloading from here or type the following command into your terminal:
    ```
    git clone https://github.com/isntlee/PopFlix
    ```
2. Navigate to this folder in your terminal.

3. A virtual environment is recommended for the Python interpreter. Enter the command:
    ```
    python -m .venv venv
    ```  
 - _Warning : **This Python command may differ** depending on operating system, the command required could be **python3** or **py**_

4. Initialize the environment by using the following command: 
    ```
    .venv\bin\activate 
    ```
 - _Warning : **This command may differ** depending on your operating system_

5. Install all the requirements and dependancies with the command 
    ```
    pip -r requirements.txt.
    ```
6. Within your IDE create a file where you can store your sensitive information for the app, I would advise an env.py file.
    ```
    from decouple import config
    SECRET_KEY = config("SECRET_KEY")
    DEBUG = config("DEBUG")
    ```
7. If you have restarted your machine to activate your environment variables, do not forget to reactivate your virtual environment with the command used at step 4.

8. Migrate the admin panel models to create your database template with the terminal command
    ```
    python manage.py migrate
    ```
9. Create your superuser to access the django admin panel and database with the following command, and then follow the steps to add your admin username and password:
    ```
    python manage.py createsuperuser
    ```
10. You can now run the program locally with the following command: 
    ```
    python manage.py runserver
    ```
11. Once the program is running, go to the local link provided and add `/admin` to the end of the url. Here log in with your superuser account.

### Dockerized Application

Please note - in order to run this container on your system, you will need this installed:
- [Docker](https://www.docker.com/) - to build and run this containerized application, add these commands to your terminal.

1. To build (if unbuilt) and start the container:
    ```
    docker-compose up -d --build
    ```

2. To run the container:
    ```
    docker build -t popflix
    ```

3. To stop and remove the container: 
    ```
    docker-compose down
    ```