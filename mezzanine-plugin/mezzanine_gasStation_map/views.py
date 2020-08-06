from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from mezzanine_gasStation_map.models import plotModel, calModel
from mezzanine_gasStation_map.forms import Plot_Form, Cal_Form
from django.conf import settings
from django.conf.urls.static import static
from django.utils import timezone

import mysql.connector
from mysql.connector import errorcode
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import openrouteservice
import requests
import pandas as pd
#import googlemaps
from itertools import tee

convtime = lambda s: '{:01}:{:02}:{:02}'.format(int(s//3600), int(s%3600//60), int(s%60))

#def index(request):
#    HttpResponse("Hello, world. You're at the polls index.")

class map(View):
    """docstring for map."""

    def __init__(self, arg):
        super(map, self).__init__()
        self.arg = arg



class map_View(View):
    initial={'key':'value'}
    #form_class=Paciente_Form
    form_class = Plot_Form
    formP_class = Plot_Form
    formC_class = Cal_Form

    template_name = 'mezzanine_gasStation_map/map.html'

    #def multiple_forms(self, request, *args, **kwargs):

    def get(self, request, *args, **kwargs):
        if request.method == 'POST':
            formPlot = self.formP_class(request.POST)
            formCal = self.formC_class(request.POST)
            if formPlot.is_valid() or formCal().is_valid():
                return HttpResponseRedirect(reverse('form-redirect'))
        else:
            formPlot = self.formP_class()
            formCal = self.formC_class()
            return render(request, self.template_name,{
                'formPlot' : formPlot,
                'formCal' : formCal
            })
        #var1 = self.kwargs['var1']
    #    form=self.form_class(initial=self.initial)
    #    return render(request, self.template_name,{'form':form})

    def post(self, request,*args, **kwargs):
        PATH_FILE = '/home/vdelaluz/public_html/gicc/static/cursos/2020-II/quantics/'
        PATH_URL = '/static/cursos/2020-II/quantics/'
        if 'execute_form_plot' in request.POST:
            form = self.form_class(request.POST)
            if form.is_valid():
                plotForm = form.save()
                with open('/home/vdelaluz/git/GasStation-LocP/db.json') as json_file:
                    config = json.load(json_file)

                states = []
                aregular = []
                apremium = []
                adiesel = []

                aregularq2 = []
                apremiumq2 = []
                adieselq2 = []
                datesq2 = []

                try:
                    cnx = mysql.connector.connect(**config)
                    cursor = cnx.cursor()

                    tnow=timezone.now()
                    today=timezone.localtime(tnow).date()

                    query = ("SELECT statec, number, datec, priceregular, pricepremium, pricediesel, nregular, npremium, ndiesel FROM pricesTime WHERE datec = CURDATE() ORDER BY datec, statec")

                    cursor.execute(query)
                    for (statec,number, datec, priceregular, pricepremium, pricediesel, nregular, npremium, ndiesel) in cursor:
                        #print(f"{statec}\t{number}\t{datec}\t{priceregular}\t{pricepremium}\t{pricediesel}\t{nregular}\t{npremium}\t{ndiesel}")

                        if(datec == today):
                            states.append(statec)
                            aregular.append(priceregular/nregular)
                            apremium.append(pricepremium/npremium)
                            adiesel.append(pricediesel/ndiesel)

                    if(plotForm.initial_date > today):
                        plotForm.initial_date=today

                    data_query = (plotForm.initial_date, plotForm.end_date, plotForm.state)
                    query = ("SELECT statec, number, datec, priceregular, pricepremium, pricediesel, nregular, npremium, ndiesel FROM pricesTime WHERE %s <= datec AND datec <= %s AND statec = %s ORDER BY datec")
                    cursor.execute(query,data_query)
                    for (statec,number, datec, priceregular, pricepremium, pricediesel, nregular, npremium, ndiesel) in cursor:
                        stateq2 = statec
                        datesq2.append(datec)
                        aregularq2.append(priceregular/nregular)
                        apremiumq2.append(pricepremium/npremium)
                        adieselq2.append(pricediesel/ndiesel)

                    if( len(datesq2) == 0 ):
                        return render(request, self.template_name,{
                            'formPlot' : formPlot,
                            'formCal' : formCal
                        })

                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                        print("Something is wrong with your user name or password")
                    elif err.errno == errorcode.ER_BAD_DB_ERROR:
                        print("Database does not exist")
                    else:
                        print(err)
                else:
                    cnx.close()

                snames=['']*32
                slist=[['AG','Aguascalientes'],['BC','Baja California'],['BS','Baja California Sur'],['CM','Campeche'],['CS','Chiapas'],['CH','Chihuahua'],['DF','Ciudad de México'],['CO','Coahuila'],['CL','Colima'],['DG','Durango'],['GJ','Guanajuato'],['GR','Guerrero'],['HG','Hidalgo'],['JA','Jalisco'],['MX','Estado de México'],['MI','Michoacán'],['MO','Morelos'],['NA','Nayarit'],['NL','Nuevo Leon'],['OA','Oaxaca'],['PU','Puebla'],['QT','Querétaro'],['QR','Quintana Roo'],['SL','San Luis Potosí'],['SI','Sinaloa'],['SO','Sonora'],['TB','Tabasco'],['TM','Tamaulipas'],['TL','Tlaxcala'],['VE','Veracruz'],['YU','Yucatan'],['ZA','Zacatecas']]
                for sl in slist:
                    snames[states.index(sl[0])]=sl[1]
                    if(stateq2 == sl[0]):
                        sname2=sl[1]
                x = np.arange(len(states))
                width = 0.25
                fig, ax = plt.subplots(figsize=(8,5))
                rects1 = ax.bar(x + 0.00, aregular, width, label='Gasolina regular')
                rects2 = ax.bar(x + 0.25, apremium, width, label='Gasolina premium')
                rects3 = ax.bar(x + 0.50, adiesel, width, label='Diesel')
                ax.set(xlabel='Estados', ylabel='Promedio de precios', title='Precios de combustibles en México '+str(today) )
                step1 = (((max(max(aregular,apremium,adiesel))+0.25)-(min(min(aregular,apremium,adiesel))-0.25))/18)
                ax.set_yticks(np.arange(min(min(aregular,apremium,adiesel))-1,max(max(aregular,apremium,adiesel))+1, step1))
                ax.set_xticks(x)
                ax.set_xticklabels(snames,rotation=90)
                ax.legend()
                ax.set_ylim(bottom=min(min(aregular,apremium,adiesel))-1)
                fig.tight_layout()
                fig.savefig(PATH_FILE+"/plotTime.png",dpi=150)
                urlpic = PATH_URL+"plotTime.png"

                dlist=[ str(day) for day in datesq2 ]
                fig2, ax2 = plt.subplots(figsize=(8,5))

                #30
                ax2.set_title("Precios de combustibles de " + dlist[0] + " a " + dlist[-1] + " en " + sname2)
                ax2.plot(dlist, aregularq2, "-o",  label="Gasoulina regular")
                ax2.plot(dlist, apremiumq2, "-o",  label=" Gasolina premium")
                ax2.plot(dlist, adieselq2, "-o", label="Diesel")
                ax2.set_xticklabels(dlist, rotation=75)
                step2 = (((max(max(aregularq2,apremiumq2,adieselq2))+0.25)-(min(min(aregularq2,apremiumq2,adieselq2))-0.25))/30)
                ax2.set_yticks(np.arange(min(min(aregularq2,apremiumq2,adieselq2))-0.25,max(max(aregularq2,apremiumq2,adieselq2))+0.25, step2))
                ax2.legend()
                ax2.grid()
                fig2.tight_layout()
                fig2.savefig(PATH_FILE+"/img/plotTime2.png",dpi=150)
                urlpic2 = PATH_URL+"/img/plotTime2.png"

                return render(request, 'mezzanine_gasStation_map/plot.html' , {'urlpic': urlpic, 'urlpic2': urlpic2})
            else:
                print('form not valid')
                return render(request, self.template_name,{
                    'formPlot' : formPlot,
                    'formCal' : formCal
                })
        elif 'execute_form_cal' in request.POST:
            form = self.formC_class(request.POST)
            if form.is_valid():
                calForm = form.save()
                if(calForm.money < 0 or calForm.economy < 0 ):
                    return render(request, self.template_name,{
                        'formPlot' : formPlot,
                        'formCal' : formCal
                    })

                with open('/home/vdelaluz/git/GasStation-LocP/db.json') as json_file:
                    config = json.load(json_file)
                try:
                    cnx = mysql.connector.connect(**config)
                    cursor = cnx.cursor()
                    data_query = (calForm.startX, calForm.startX, calForm.startY)
                    #SELECT places.place_id,places.name,(acos(sin(radians(20.135936)) * sin(radians(places.Y)) + cos(radians(20.135936)) * cos(radians(places.Y)) * cos(radians(-102.744064) - radians(places.X))) * 6378) as distance,places.x,places.y,prices.regular,prices.premium,prices.diesel,places.state FROM places LEFT JOIN prices ON places.place_id = prices.prices_place_id ORDER BY distance LIMIT 5;
                    query = ("SELECT places.place_id,places.name,(acos(sin(radians(%s)) * sin(radians(places.Y)) + cos(radians(%s)) * cos(radians(places.Y)) * cos(radians(%s) - radians(places.X))) * 6378) as distance,places.x,places.y,prices.regular,prices.premium,prices.diesel,places.state FROM places LEFT JOIN prices ON places.place_id = prices.prices_place_id WHERE prices.regular IS NOT NULL ORDER BY distance LIMIT 50")
                    cursor.execute(query,data_query)
                    places = []
                    loclist = []
                    glist = ""
                    with open('/home/vdelaluz/git/GasStation-LocP/key.json') as json_file:
                        keys = json.load(json_file)

                    for a in cursor:
                        place = { 'type' : 'Feature' , 'geometry' : { 'type' : 'Point' , 'coordinates' : [ a[3] , a[4] ] }}
                        properties={ 'name' : a[1] , 'distance' : a[2] , 'money' : calForm.money, 'economy' : calForm.economy , 'startX' : calForm.startX, 'startY': calForm.startY}
                        if(a[5]!=None):
                            properties['regular']=a[5]
                        if(a[6]!=None):
                            properties['premium']=a[6]
                        if(a[7]!=None):
                            properties['diesel']=a[7]
                        if(a[8]!=None):
                            properties['state']=a[8]
                        place['properties']=properties
                        places.append(place)
                        loclist.append([ a[3] , a[4] ])
                        glist+=str(a[3])+","+str(a[4])+"|"
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                        print("Something is wrong with your user name or password")
                    elif err.errno == errorcode.ER_BAD_DB_ERROR:
                        print("Database does not exist")
                    else:
                        print(err)
                else:
                    cnx.close()
                body = {"locations":[[calForm.startY,calForm.startX]]+loclist,"destinations":[0],"metrics":["distance","duration"],"units":"km"}
                headers = {
                'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
                'Authorization': keys['ORSkey'],
                'Content-Type': 'application/json; charset=utf-8'
                }
                call = requests.post('https://api.openrouteservice.org/v2/matrix/driving-car', json=body, headers=headers)
                reqORS = call.json()
                #googlemaps-4.4.2
                #callG = requests.post("https://maps.googleapis.com/maps/api/distancematrix/json?origins="+str(calForm.startY)+","+str(calForm.startX)+"&destinations="+glist[:-1]+"&departure_time=now&key="+keys['cloudKey'])
                #reqG = callG.json()
                #print(reqG)
                for i in range(len(places)):
                    try:
                        places[i]['properties']['realdistance'] = '%.3f'%(float(reqORS['distances'][i+1][0]))
                    except Exception as e:
                        places[i]['properties']['realdistance'] = '%.3f'%(float(places[i]['properties']['distance']))

                    try:
                        places[i]['properties']['duration'] = convtime(reqORS['durations'][i+1][0])
                    except Exception as e:
                        places[i]['properties']['duration'] = "00:00:00"

                    places[i]['properties']['spend'] = '%.3f'%((float(places[i]['properties']['realdistance'])/float(calForm.economy)))
                    if('regular' in places[i]['properties']):
                        spendr = '%.3f'%(float(places[i]['properties']['spend'])*float(places[i]['properties']['regular']))
                        places[i]['properties']['realmoneyr'] = '%.3f'%(float(calForm.money) - float(spendr))
                        places[i]['properties']['realGasr'] = '%.3f'%(float(places[i]['properties']['realmoneyr']) / float(places[i]['properties']['regular']))
                        places[i]['properties']['litrosr'] = '%.3f'%(float(calForm.money) / float(places[i]['properties']['regular']))
                    if('premium' in places[i]['properties']):
                        spendp = '%.3f'%(float(places[i]['properties']['spend'])*float(places[i]['properties']['premium']))
                        places[i]['properties']['realmoneyp'] = '%.3f'%(float(calForm.money) - float(spendp))
                        places[i]['properties']['realGasp'] = '%.3f'%(float(places[i]['properties']['realmoneyp']) / float(places[i]['properties']['premium']))
                        places[i]['properties']['litrosp'] = '%.3f'%(float(calForm.money) / float(places[i]['properties']['premium']))
                    if('diesel' in places[i]['properties']):
                        spendd = '%.3f'%(float(places[i]['properties']['spend'])*float(places[i]['properties']['diesel']))
                        places[i]['properties']['realmoneyd'] = '%.3f'%(float(calForm.money) - float(spendd))
                        places[i]['properties']['realGasd'] = '%.3f'%(float(places[i]['properties']['realmoneyd']) / float(places[i]['properties']['diesel']))
                        places[i]['properties']['litrosd'] = '%.3f'%(float(calForm.money) / float(places[i]['properties']['diesel']))

                #print(places)
                doc={ 'type' : 'FeatureCollection' , 'features' : places }
                print(doc)
                with open(PATH_FILE+'/js/tmp.json', 'w') as outfile:
                    json.dump(doc, outfile, indent=4, sort_keys=True)
                return render(request, 'mezzanine_gasStation_map/request.html')
            else:
                print('form not valid')
                return render(request, self.template_name,{
                    'formPlot' : formPlot,
                    'formCal' : formCal
                })

        return HttpResponseRedirect('/')


#@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(map_View, self).dispatch(*args, **kwargs)
