import json
import subprocess
import psycopg2
import os

try:
    cnx = psycopg2.connect(os.getenv('DATABASE_URL', 'Optional default value'))
    cursor = cnx.cursor()
    updatestates = "INSERT INTO pricesTime(statec,number,datec,priceregular,pricepremium,pricediesel,nregular,npremium,ndiesel) SELECT tmp.state, tmp.numberplaces ,tmp. today, tmp.pricer, tmp.pricep, tmp.pricep, tmp.numberr, tmp.numberp, tmp.numberd FROM ( SELECT places.state AS state, COUNT(*) AS numberplaces, TIMEZONE('America/Mexico_City',NOW())::DATE AS today, SUM(regular) AS pricer, SUM(premium) AS pricep, SUM(diesel) AS priced, COUNT(regular) AS numberr, COUNT(premium) AS numberp, COUNT(diesel) AS numberd FROM places LEFT JOIN prices ON places.place_id = prices.prices_place_id WHERE state is not null GROUP BY places.state ) AS tmp ON CONFLICT (statec,datec) DO UPDATE SET priceregular = EXCLUDED.priceregular, pricepremium = EXCLUDED.pricepremium, pricediesel = EXCLUDED.pricediesel, nregular = EXCLUDED.nregular, npremium = EXCLUDED.npremium, ndiesel = EXCLUDED.ndiesel"
    query=("SELECT places.place_id,places.name,places.cre_id,places.x,places.y,prices.regular,prices.premium,prices.diesel,places.state FROM places LEFT JOIN prices ON places.place_id = prices.prices_place_id")
    cursor.execute(updatestates)
    cursor.execute(query)
    places=[]

    for a in cursor:
        place = { 'type' : 'Feature' , 'geometry' : { 'type' : 'Point' , 'coordinates' : [ a[3] , a[4] ] }}
        properties={ 'name' : a[1] }
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

    #f= open(PublicPATH+"data.json","w+")
    doc={ 'type' : 'FeatureCollection' , 'features' : places }
    with open('mezzanine-plugin/mezzanine_gasStation_map/static/'+'js/data.json', 'w') as outfile:
        json.dump(doc, outfile, indent=4, sort_keys=True)
        print('mezzanine-plugin/mezzanine_gasStation_map/static/'+"js/data.json")
    #output = subprocess.run(["scp",PublicPATH+"data.json","quantics@132.247.186.67:public_html/static"])

    cnx.commit()
except psycopg2.Error as err:
    print(err)
else:
    cnx.close()
