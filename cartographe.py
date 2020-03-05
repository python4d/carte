"""
CARTE DE LA FRANCE ET DE SES DEPARTEMENTS AVEC DEGRADE SUIVANT UN CRITERE 
(ici le nb de salariés d'une entreprise)
PYTHON4D Mars2020
"""

import folium
import os,math
import json 
import requests
import branca.colormap as cm
import pandas as pd
from shapely.geometry import shape

dir=os.getcwd()
#
# dource des données de frontières des départements
# url='https://france-geojson.gregoiredavid.fr/repo/departements.geojson'
#
path=f'{dir}\\departements.geojson.txt'
with open(path) as json_file:
    geo_json_data = json.load(json_file)

#
#récupération des données des départements et calcul du centre des ces départements
#
dp=geo_json_data["features"]
infos_DP=[]
for i in dp: 
    zone = shape(i['geometry'])
    infos_DP.append([i['properties']['code'],i['properties']['nom'],(zone.centroid.x,zone.centroid.y)])
    

#
# liste du nombre des salariés des départements
# utilisation stricte des noms de département des données ci dessus
#
nb_salaries = pd.read_csv("nb_salariés_par_département - 1.csv")
stat_salaries = nb_salaries.set_index('DP')['Nb_Salaries']

#centrage de la carte sur la France
coords = (47.5,2.5840685)
#objet map vierge issu d'OpenStreetMap
map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=7)
#création du colormap de carte
#cf http://soliton.vm.bytemark.co.uk/pub/cpt-city/cb/seq/index.html
colormap = cm.linear.YlGnBu_09.scale(0, 80).to_step(10)
#colormap = cm.linear.YlOrRd_05.scale(0, 100).to_step(10)
colormap.caption = 'Nb de Salariés'
map.add_child(colormap)

#Gestion des données des frontières des départements
folium.GeoJson(
    geo_json_data,
    style_function=lambda feature: {
        'fillOpacity': 0.9,
        'fillColor': colormap(stat_salaries[feature['properties']['nom']]),
        'color': 'black',
        'weight': 2, 
    }
).add_to(map)

#Ecriture des noms des départements
for i in infos_DP:
    str=f"{i[1].replace('-','.')}.{int(stat_salaries[i[1]])}"
    folium.Marker(location=[i[2][1],i[2][0]-0.1],icon=folium.DivIcon(html=f"""<div style="font-size: 6pt; color : black">{str}</div>""")).add_to(map)

#Sauvegarde du HTML de la map totalement autonome
map.save(outfile='map.html')

