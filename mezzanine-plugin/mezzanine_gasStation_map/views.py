from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from mezzanine_gasStation_map.models import plotModel
from mezzanine_gasStation_map.forms import Plot_Form
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


#def index(request):
#    HttpResponse("Hello, world. You're at the polls index.")

class map(View):
    """docstring for map."""

    def __init__(self, arg):
        super(map, self).__init__()
        self.arg = arg

class map_View(View):
    initial={'kay':'value'}
    #form_class=Paciente_Form
    form_class = Plot_Form
    template_name = 'mezzanine_gasStation_map/map.html'

    def get(self, request, *args, **kwargs):
        #var1 = self.kwargs['var1']
        form=self.form_class(initial=self.initial)
        return render(request, self.template_name,{'form':form})

    def post(self, request,*args, **kwargs):
        if 'execute_page_button' in request.POST:
            form = self.form_class(request.POST)
            if form.is_valid():
                plotForm = form.save()
                PATH_FILE = '/home/user/git/GasStation-LocP/mezzanine-plugin/mezzanine_gasStation_map/static/img/'
                PATH_URL = '/static/mezzanine_gasStation_map/img/'
                with open('/home/user/git/GasStation-LocP/db.json') as json_file:
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
                        print(f"{statec}\t{number}\t{datec}\t{priceregular}\t{pricepremium}\t{pricediesel}\t{nregular}\t{npremium}\t{ndiesel}")

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
                        return render(request, self.template_name, {'form': form})

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
                fig2.savefig(PATH_FILE+"/plotTime2.png",dpi=150)
                urlpic2 = PATH_URL+"plotTime2.png"


                return render(request, 'mezzanine_gasStation_map/plot.html' , {'urlpic': urlpic, 'urlpic2': urlpic2})
            else:
                print('form not valid')
                return render(request, self.template_name, {'form': form})

        return HttpResponseRedirect('/')



#@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(map_View, self).dispatch(*args, **kwargs)
