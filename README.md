
# **Popflix**

This is a Django REST based media manager designed with an adaptive & hierarchical file structure. Popflix would function as an ideal API back-end for any media manager project whether the key file type was audio, video, text etc, etc. There is a full choice of bonus features including a testing suite, advanced filtering, containerization and CI/CD prebuilt.    

<br>

- [**Table of Contents:**](#table-of-contents)
    - [**Features**](#features)
    - [**Technologies**](#technologies)
    - [**Deployment**](#deployment)
    - [**Database Design**](#database-design)
    
<br>

## Features:

**API**
- Adaptive API allowing completely arbitrary depth of channels/objects, see location:
    ```
    contents\api
    ```

**Channel rating command**
- Depth-first search algorithm to trace all nodes (channel's ratings), summing them on each branch (superchannel) backtracking to root (origin channel).
- To run this management command, add below to terminal:

    ```
    python manage.py channel_ratings
    ```
 - _Warning : **This command may differ** depending on operating system, the command required could be **python3** or **py**_

**Filtering**
- Category (Groups) options available to each superchannel that can be easily query filtered. 
- Add query statement below as suffix to active superchannel url:

    ```
    ?group=name_of_group
    ```

**Testing suite**
- Unit testing accommodates all project features with test coverage of over 93%.
- To run coverage tests, use this command in terminal:

    ```
    coverage run --source='.' manage.py test
    ```
- Coverage report available with command:

    ```
    coverage report
    ```

<br>

## Explanations:
These notes develop on the more complex and interesting parts of the project

<br>

**Channel rating command**
- A management command that calculates the average rating for each active Channel and its subchannels.
  It uses depth-first traversal to aggregate subchannel ratings and then calculates averages

    Noteworthy methods: 
    - `handle` executes the command, calling `get_channel_ratings` and writing the results to a csv file.
    - `get_channel_ratings` processes each active Channel, computes average ratings including subchannels.
    - `get_all_subchannels` performs an iterative depth-first traversal of a Channel hierarchy, 
       collecting and returning all visited Channels and their aggregate ratings, while optionally 
       including the starting Channel itself.

<br>

**API ListView**
- A view for listing channels with several overrides.

    - Overridden dispatch method for handling URL validation and routing.
      Also handles the extraction of a `group` parameter from the GET request.

    - The get_queryset method is overridden to provide a queryset that filters
      channels based on a `channel` or an optional `group` channel parameter.

<br>

**API URL pattern**:
- URL pattern for the ListView with a dynamic path and optional group parameter.

    - This pattern captures a path and an optional group from the URL, passing them as
        arguments to the ListView view. The path is required, while the group is optional
        and can be omitted from the URL. Path is the hierarchy of Channels

<br>

**API URL validator**
- A utility class for validating URLs against channel and content slugs.
    
    - This class provides static methods to check the existence of channels and contents
      based on the slug and ensures that the URL matches the hierarchy of superchannels.

<br>

**Channel model**
- Represents a channel instance.

    Noteworthy fields: 
    - `groups` allows channels to be part of multiple Groups as it's set as a many-to-many relationship.
    - `superchannel` creates a hierarchical relationship between Channels as foreign key to another Channel/'self'

    Noteworthy methods: 
    - `save` sets the slug and potentially updates related superchannels' Groups.
    - `get_all_superchannels` gets a list of all superchannels for a Channel, optionally including the Channel itself.
    - `add_group_to_superchannels` adds the Channel's Groups to all of its superchannels.

<br>    

 **ChannelManager**:
- Custom model manager to retrieve and filter Channels.

    - The method, `get_channels_by_group` filters a given queryset of channels by a group name.

<br>

## Technologies:

- **Python**    
    - [Python 3.11.0](https://www.python.org/) - Used as base language.
- **Django**
    - [Django 4.2.8](https://www.djangoproject.com/) - A Python web framework for rapid development.
    - [Django REST 3.14.0](https://www.django-rest-framework.org/) - Django-based toolkit for building Web APIs.
- **Database**
    - [SQlite](https://www.sqlite.org/index.html) - For a development database, provided by Django.
- **Docker**
    - [Docker](https://www.docker.com/) - Platform designed to help build, share, and run container applications.
- **Testing**    
    - [Coverage 7.4.1](https://pypi.org/project/coverage/) - Code coverage measurement for Python.
- **CI/CD**
    - [GitHub Actions](https://github.com/features/actions) - Build, test, and deploy from your remote storage.

<br>

## Deployment:

### Local Deployment:

Please note - in order to run this project locally on your own system, you will need the following installed:
- [Python3](https://www.python.org/) to run the application.
- [PIP](https://pip.pypa.io/en/stable/) to install app requirements.
- [GIT](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) for version control.

1. Clone the Popflix repository by either downloading from here or type the following command into your terminal:
    ```
    git clone https://github.com/isntlee/PopFlix
    ```
2. Stay in your current folder, don't navigate into Popflix yet

3. A virtual environment is recommended for the Python interpreter. Enter the command:
    ```
    python -m venv venv
    ```  
 - _Warning : **This Python command may differ** depending on operating system, the command required could be **python3** or **py**_

4. Navigate into Popflix and initialize the virtual environment by using the following command: 
    ```
    ..\venv\Scripts\Activate.ps1 
    ```
 - _Warning : **This command may differ** depending on your operating system_

5. Install all the requirements and dependancies with the command:
    ```
    pip install -r requirements.txt
    ```
6. Migrate the admin models to create your database template with the terminal command:
    ```
    python manage.py migrate
    ```
7. Create your superuser to access the django admin panel and database with the following command:
    ```
    python manage.py createsuperuser
    ```
8. Enter these details for the initial superuser. Ignore all warnings, don't add an email. Change the User password afterwards as this password is exposed. However, if you plan to add the prebuilt data below, you'll need these details to login, change User password after that.
    ```
    Username = iam_the_law -- Password = 2000
    ```
9. You can now run the program locally with the following command: 
    ```
    python manage.py runserver
     ```
10. Once the program is running, go to localhost and add `/admin/` to the end of the url. Here log in with the initial superuser account.

11. Create env.py file at root level where you can store your sensitive information for the app. Add these details to that file:
    ```
    SECRET_KEY = "SECRET_KEY"
    DEBUG = "DEBUG"
    ```
12. Create a new and truly secret key, which will be generated in a secret_key.txt file at root level, with this command:
    ```
    python core/generate_key.py
    ```
13. Find the SECRET_KEY and DEBUG variables in the core/settings.py file. You'll find two sets of SECRET_KEY and DEBUG variables: commented out and uncommented. You should comment out the uncommented, and vice-versa.

14. Finally, set the variables in your .env file. Set SECRET_KEY to the text found in secret_key.txt, remember to add '' as it should be a string. Set DEBUG to whatever you prefer, there are no security problems with DEBUG = 'True' in development. Do change for production. 

15. If you would like to start with Channel/Content/User test data, then run this command: 
    ```
    python manage.py loaddata data/popflix_data.json
    ```

<br>

### Dockerize Application:

Please note - in order to run this container on your system, you will need Docker installed on your system. And, some working knowledge.
- [Docker](https://www.docker.com/) - to build and run this containerized application, add these commands to your terminal:

1. To build (if unbuilt) and start the container in detatched mode:
    ```
    docker-compose up -d
    ```

2. To stop and remove the container: 
    ```
    docker-compose down
    ```

3. To use the relevant local deployment instructions above, prefix the commands with: 
    ```
    docker-compose exec web
    ```

<br>

## Database Design:

- [SQlite3](https://www.sqlite.org/index.html) - For development database, provided by Django.

### Data Models:

**Users**

The User model utilized for this project is the standard one provided by **`django.contrib.auth.models`**

\
**Group model**

| Name | Key in DB | Validation | Field Type |
--- | --- | --- | ---
Title | title | max_length=250 | CharField
Active | active | default=True, null=True | BooleanField
Picture Url | picture_url | max_length=250, null=True, blank=True | URLField
Slug | slug | max_length=250, unique=True, null=True, blank=True | SlugField

\
**Channel model**

| Name | Key in DB | Validation | Field Type |
--- | --- | --- | ---
Title | title | max_length=250 | CharField
Language | language | max_length=250 | CharField
Active | active | default=True, null=True | BooleanField
Picture Url | picture_url | max_length=250, null=True, blank=True | URLField
Groups | groups | blank=True | ManyToManyField
Slug | slug | max_length=250, unique=True, null=True, blank=True | SlugField
Superchannel | superchannel | on_delete=models.SET_NULL, null=True, blank=True | ForeignKey

\
**Content model**

| Name | Key in DB | Validation | Field Type |
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

<br>