#!/usr/bin/python3

import folium as fl
import cherrypy

from pandas import DataFrame
from pandas import Series
from typing import List

import os

def getMapOSMVisitedPointsPage(userId:int):

    visitedGPS:List = cherrypy.session['visitedGPSCoords']
    visitedDescrs:List = cherrypy.session['visitedDescrs']

    #visitedGPS = [(40.71937995021471, -73.98542770834685)]
    #visitedDescrs = [1]

    return getMapOSMPointsPage(visitedGPS, visitedDescrs)

def getMapOSMRecommendedPointsPage(userId: int):
    recGPS:List = cherrypy.session['recGPSCoords']
    recDescrs:List = cherrypy.session['recDescrs']

    return getMapOSMPointsPage(recGPS, recDescrs)

def getMapOSMPointsPage(visitedGPS, visitedDescrs):

    myMap = fl.Map((visitedGPS[0][0], visitedGPS[0][1]), zoom_start=13)
    for gpsI,descrI in zip(visitedGPS, visitedDescrs):
        marker = fl.Marker([gpsI[0], gpsI[1]], tooltip=descrI)  # latitude,longitude
        myMap.add_child(marker)

    myMap.fit_bounds(myMap.get_bounds(), padding=(50, 50))

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