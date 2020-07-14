=============
mezzanine_gasStation_map
=============

Plugin for mezzanine

Quick start
------------

1.-Install leaflet for django::

    pip install django-leaflet
    pip install folium
    pip install shapely

2.- Add mezzanine map to INSTALLED_APPS::

  INSTALLED_APPS = [
    ...
    'leaflet',
    'mezzanine_gasStation_map',
    ...
  ]

3.- Include in yourProject/yourProject/urls.py::

  import mezzanine_gasStation_map.urls

4.- Include the polls URLconf in yourProject/yourProject/urls.py like this::

    url('map/', include('mezzanine_gasStation_map.urls')),


5.- Create links in yourProject::

    ln -s /home/user/git/GasStation-LocP/mezzanine-plugin/mezzanine_gasStation_map .
    ln -s /home/user/git/GasStation-LocP/mezzanine-plugin/mezzanine_gasStation_map/static ./static/mezzanine_gasStation_map
    ln -s /home/user/git/GasStation-LocP/mezzanine-plugin/mezzanine_gasStation_map/templates ./templates/mezzanine_gasStation_map
