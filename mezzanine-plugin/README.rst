=============
mezzanine_gasStation_map
=============

Plugin for mezzanine

Quick start
------------

1.-Install libreries ::

  pip install django-leaflet==0.20.0
  pip install matplotlib==3.0.2
  pip install mysql==0.0.2
  pip install mysql-connector==2.2.9
  pip install mysql-connector-python==8.0.21
  pip install mysqlclient==1.4.6
  pip install numpy==1.61.2
  pip install scrapy==2.0.0
  pip install urllib3==1.24.2
  pip install openrouteservice==2.3.0
  pip install shapely==1.7.0
  pip install setuptools=40.8.0

2.- Add mezzanine map to INSTALLED_APPS in yourProject/yourProject/settings.py ::

  INSTALLED_APPS = [
    ...
    'leaflet',
    'mezzanine_gasStation_map',
    ...
  ]

3.- Check the correct timezone in yourProject/yourProject/settings.py, in # MAIN DJANGO SETTINGS #, example ::

  TIME_ZONE = 'America/Mexico_City'

4.- Include in yourProject/yourProject/urls.py ::

  import mezzanine_gasStation_map.urls

5.- Include the mezzanine_gasStation_map URLconf in yourProject/yourProject/urls.py inside urlpatterns like this ::

    url('map/', include('mezzanine_gasStation_map.urls')),


6.- Create links in yourProject ::

    ln -s /home/< user >/git/GasStation-LocP/mezzanine-plugin/mezzanine_gasStation_map .
    ln -s /home/< user >/git/GasStation-LocP/mezzanine-plugin/mezzanine_gasStation_map/static ./static/mezzanine_gasStation_map
    ln -s /home/< user >/git/GasStation-LocP/mezzanine-plugin/mezzanine_gasStation_map/templates ./templates/mezzanine_gasStation_map

7.- Get your key in https://openrouteservice.org/ and add in key.json ::

{ "ORSkey" : "YOUR_API_KEY" }

8.- Set all you routes for your project ::

  routes.json: lines 2 and 3
  mezzanine-plugin/mezzanine_gasStation_map/views.py: lines 68, 74, 192 and 204


9.- Make migrates and migrate in your your project ::

    $ python3 manage.py makemigrations mezzanine_gasStation_map
    $ python3 manage.py migrate
