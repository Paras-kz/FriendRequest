#Description -- This Django project, is for creating api for performing crud operations on friend requests. In this authenticated users can
send friend request(upto 3/min), delete, modify and also list their friend list.

#Steps to setup --

-Cloning git repo: git clone <this repo url>

-Navigate to the project directory: cd social_network

-Create and activate a virtual environment: python -m venv venv

-Activate Venv: venv\Scripts\activate

-Install project dependencies: pip install -r requirements.txt

-Apply migrations: python manage.py migrate

-Create a superuser for accessing the admin interface: python manage.py createsuperuser
