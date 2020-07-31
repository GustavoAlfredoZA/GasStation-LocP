from django.db import models
from django.apps.config import MODELS_MODULE_NAME
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class plotModel(models.Model):
    STATE_CHOICES = (
    ('AG','Aguascalientes'),
    ('BC','Baja California'),
    ('BS','Baja California Sur'),
    ('CM','Campeche'),
    ('CS','Chiapas'),
    ('CH','Chihuahua'),
    ('DF','Ciudad de México'),
    ('CO','Coahuila'),
    ('CL','Colima'),
    ('DG','Durango'),
    ('GJ','Guanajuato'),
    ('GR','Guerrero'),
    ('HG','Hidalgo'),
    ('JA','Jalisco'),
    ('MX','Estado de México'),
    ('MI','Michoacán'),
    ('MO','Morelos'),
    ('NA','Nayarit'),
    ('NL','Nuevo Leon'),
    ('OA','Oaxaca'),
    ('PU','Puebla'),
    ('QT','Querétaro'),
    ('QR','Quintana Roo'),
    ('SL','San Luis Potosí'),
    ('SI','Sinaloa'),
    ('SO','Sonora'),
    ('TB','Tabasco'),
    ('TM','Tamaulipas'),
    ('TL','Tlaxcala'),
    ('VE','Veracruz'),
    ('YU','Yucatan'),
    ('ZA','Zacatecas'),
    )

    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    tnow=timezone.now()
    today=str(timezone.localtime(tnow).date())

    initial_date = models.DateField("Fecha de inicio", default=today)
    end_date = models.DateField("Fecha final", default=today)

class calModel(models.Model):
    startX = models.FloatField("Latitud (aproximación)")
    startY = models.FloatField("Longitud (aproximación)")
    economy = models.FloatField("Rendimiento de tu automovil (km/lt)")
    money = models.FloatField("Cuanto dinero tienes para comprar gasolina (MXN)")


class Place(models.Model):
    name = models.CharField(max_length=128)
    cre_id = models.CharField(max_length=32)
    place_id = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return self.place

class Prices(models.Model):
    prices_place_id = models.IntegerField()
    regular = models.FloatField()
    premium = models.FloatField()
    diesel = models.FloatField()

    def __str__(self):
        return self.prices



#from djgeojson.fields import PolygonField
#from django.db import models
#
#class MapSpot(models.Model):

#    title = models.CharField(max_length=256)
#    description = models.TextField()
#    picture = models.ImageField()
#    geom = PolygonField()
#
#    def __str__(self):
#        return self.title
#
#    @property
#    def picture_url(self):
#        return self.picture.url
