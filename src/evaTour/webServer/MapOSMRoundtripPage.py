#!/usr/bin/python3

import folium as fl
import cherrypy
import os

def getMapOSMRoundtripPage(row=0, column=0):

    indivGPSDict = cherrypy.session['indivGPSDict']
    indivDict = cherrypy.session['indivDict']
    fitnessDict = cherrypy.session['fitnessDict']

    gpsCoords = indivGPSDict[int(column)]
    descrs = indivDict[int(column)]
    fitness = fitnessDict[int(column)]

#    print("column: " + str(column))
#    print("gpsCoords: " + str(gpsCoords))
#    print("descrs: " + str(descrs))
#    print("fitness: " + str(fitness))

    #if column == "0":
    #    gpsCoords = [(40.71937995021471, -73.98542770834685), (40.72651075083395, -73.98171901702881), (40.73528249691621, -73.99040315158283), (40.74148072635098, -74.00943275021737), (40.747141, -74.00717854499817), (40.74706188749892, -74.00519371032715), (40.74143709197248, -73.99324416730772), (40.74218830848454, -73.98792418909154), (40.756070596303616, -73.98452667169322), (40.75696867739112, -73.98895146714219), (40.75705162247207, -73.98595570238331), (40.75977271753036, -73.9799984680946), (40.76750161421655, -73.99061002177434), (40.7714256153356, -73.97350072860723), (40.76428720689057, -73.98384371752819), (40.77361447158453, -73.9641058682518), (40.78299485153325, -73.95890951156616), (40.7931947810883, -73.95184545934148), (40.80968414945981, -73.95017623901367), (40.82411234141161, -73.91566813441439), (40.72108603096943, -73.95210950256656), (40.70523754289766, -73.93034934997559), (40.69118178774824, -73.97480964660645), (40.67684099295394, -73.98323536975668), (40.70391994183744, -73.98639678955078), (40.70314726242412, -74.00966763496399), (40.721720259364965, -74.0063167982994), (40.73083612189599, -73.99764060974121), (40.7248181, -73.994414), (40.71397514115215, -73.99871320357333)]
    #    descrs = [22, 27, 21, 37, 46, 33, 32, 31, 48, 30, 40, 42, 45, 41, 34, 49, 43, 44, 23, 26, 25, 36, 38, 39, 47, 20, 35, 29, 24, 28]
    #bestIndivGPS = convertIndividualToGPS(descrs, self.itemsDF)

    myMap = fl.Map((gpsCoords[0][0], gpsCoords[0][1]), zoom_start=13)
    for gpsI,descrI in zip(gpsCoords, descrs):
        marker = fl.Marker([gpsI[0], gpsI[1]], tooltip=descrI)  # latitude,longitude
        myMap.add_child(marker)

    wind_line = fl.PolyLine(gpsCoords + [gpsCoords[0]], weight=15, color='#8EE9FF')
    myMap.add_child(wind_line)

    myMap.fit_bounds(myMap.get_bounds(), padding=(30, 30))

    myMap.get_root().render()
    header = myMap.get_root().header.render()
    body_html = myMap.get_root().html.render()
    script = myMap.get_root().script.render()

    return             """
            <!DOCTYPE html>
            <html>
                <head>
                    """ + header + """
                </head>
                <body>
                    """ + body_html + """
                    <script>
                    """ + script + """
                    </script>
                </body>
            </html>
        """