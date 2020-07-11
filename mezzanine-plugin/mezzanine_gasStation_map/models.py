from django.db import models

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
