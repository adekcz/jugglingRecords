## Synopsis
We want to create simple and uncluttered website that aggregates juggling records. 



## devel notes
pip install django-nocaptcha-recaptcha
pip install pylint-django
pip install django-widget-tweaks #this is absolutely necessary

pylint --load-plugins pylint_django 


python manage.py makemigrations 
python manage.py migrate
