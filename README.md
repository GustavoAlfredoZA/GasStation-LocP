# Petrol and diesel stations
## Definition
This project came up thanks to a spontaneous idea, realizing that it had a great future, so we decided to make an interface to improve the purchase of gasoline, reducing their money or reducing distance to buy it using data from the Energy Regulatory Commission, which will be downloaded through a script that we will make.
## Overall Objectives
The objective of this project is to help people make decisions about where to buy their gasoline, the place that is closest to them but at the same time convenient for them in terms of price, among other things. One of the examples that we try to reduce is when you want to go to a gas station that is cheaper but is very far away, so you will get the same, you should go to one that is closer but is a little more expensive, so with this project we try to decide this type of issues.
## Software
In this project, most of the code is in Python with libraries like Pandas, Scrapy and some data visualization libraries, and some technology to work with maps, routes and layers.
## Data source
Our data source comes from the Energy Regulatory Commission, which is the Coordinated Energy Regulatory Body promoting the efficient development of the sector and the reliable supply of hydrocarbons and electricity.
https://datos.gob.mx/busca/dataset/estaciones-de-servicio-gasolineras-y-precios-finales-de-gasolina-y-diesel .
## Data collection
The process to obtain the data is through GasStation.by, which first extracts the download URL from the xml files using Scrapy, then sets the names to 0 for places and 1 for prices, plus the download datatime with extention xml , finally, they are added to a record csv with names date and type.
