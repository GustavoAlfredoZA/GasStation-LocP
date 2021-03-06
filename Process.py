import json
import mysql.connector
from mysql.connector import errorcode
import subprocess

p = open("routes.json")
routes = json.load(p)
ProyectPATH=routes['proyect']
PublicPATH=routes['public']
p.close()

with open('db.json') as json_file:
    config = json.load(json_file)

try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    updatestates = "INSERT INTO pricesTime(statec,number,datec,priceregular,pricepremium,pricediesel,nregular,npremium,ndiesel) SELECT tmp.state, tmp.numberplaces ,tmp. today, tmp.pricer, tmp.pricep, tmp.pricep, tmp.numberr, tmp.numberp, tmp.numberd FROM ( SELECT places.state AS state, COUNT(*) AS numberplaces, CURDATE() AS today, SUM(regular) AS pricer, SUM(premium) AS pricep, SUM(diesel) AS priced, COUNT(regular) AS numberr, COUNT(premium) AS numberp, COUNT(diesel) AS numberd FROM places LEFT JOIN prices ON places.place_id = prices.prices_place_id WHERE state is not null GROUP BY places.state ) AS tmp ON DUPLICATE KEY UPDATE priceregular = tmp.pricer, pricepremium = tmp.pricep, pricediesel = tmp.priced, nregular = tmp.numberr, npremium = tmp.numberp, ndiesel = tmp.numberd"
    query=("SELECT places.place_id,places.name,places.cre_id,places.x,places.y,prices.regular,prices.premium,prices.diesel,places.state FROM places LEFT JOIN prices ON places.place_id = prices.prices_place_id")
    cursor.execute(updatestates)
    cursor.execute(query)
    places=[]

    for a in cursor:
        #place={'name' : a[1],'cre_id' : a[2], 'x' : a[3], 'y' : a[4]}


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
    with open(PublicPATH+'js/data.json', 'w') as outfile:
        json.dump(doc, outfile, indent=4, sort_keys=True)
        print(PublicPATH+"js/data.json")
    #output = subprocess.run(["scp",PublicPATH+"data.json","quantics@132.247.186.67:public_html/static"])

    cnx.commit()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()
