#!/usr/bin/python3

from typing import List

class Maps(object):

   def getMaps(self):
      points = self.getPoints()
      
      resultStr:str = ""
      resultStr += self.getMap('1', points)
      resultStr += self.getMap('2', points)
      resultStr += self.getMap('3', points)
      resultStr += self.getMap('4', points)
      return resultStr

   def getMap(self, mapID:str, points):
      resultStr:str = """var center"""+mapID+""" = SMap.Coords.fromWGS84(14.41790, 50.12655);
var map"""+mapID+""" = new SMap(JAK.gel('map"""+mapID+"""'), center"""+mapID+""", 13);
map"""+mapID+""".addDefaultLayer(SMap.DEF_BASE).enable();
map"""+mapID+""".addDefaultControls();

var layer"""+mapID+""" = new SMap.Layer.Geometry();
map"""+mapID+""".addLayer(layer"""+mapID+""");
layer"""+mapID+""".enable();


var points"""+mapID+""" = [
"""
      pointsListOfStr:List[str] = ['('+str(pLatI)+', '+str(pLongI)+') ' for pLatI, pLongI in points]
      
      pointsStr = ''.join(pointsListOfStr)
      pointsStr = pointsStr.replace(") (", "), (")
      pointsStr = ''.join(pointsStr).replace("(", "SMap.Coords.fromWGS84(")
      
      resultStr += pointsStr 
      resultStr += """
];
var options"""+mapID+""" = {
    color: "#f00",
    width: 3
};
var polyline"""+mapID+""" = new SMap.Geometry(SMap.GEOMETRY_POLYLINE, null, points"""+mapID+""", options"""+mapID+""");
layer"""+mapID+""".addGeometry(polyline"""+mapID+""");

//var znacky = new SMap.Layer.Marker();
//m.addLayer(znacky);
//znacky.enable();
//var def = {
//    "Bod A": bodA,
//    "Bod B": bodB,
//    "Střed": center
//}
//var o = {};
//for (var title in def) {
//    o.title = title;
//    znacky.addMarker(new SMap.Marker(def[title], null, o));
//}
"""
      return resultStr

   def getPoints(self):
      points:List[tuple] = [(14.438895, 50.136554),(14.418895, 50.116554), (14.417895, 50.126554), (14.426672, 50.123787), (14.413489, 50.129343), (14.417963, 50.120933), (14.418537, 50.126094), (14.422892, 50.127521), (14.420757, 50.123295)]
      return points
      
      
   def getMapI(self, mapID:str=0):
      resultStr:str = """var center"""+str(mapID)+""" = SMap.Coords.fromWGS84(14.41790, 50.12655);
var map"""+str(mapID)+""" = new SMap(JAK.gel('map"""+str(mapID)+"""'), center"""+str(mapID)+""", 13);
map"""+str(mapID)+""".addDefaultLayer(SMap.DEF_BASE).enable();

map"""+str(mapID)+""".addDefaultControls();
"""
      return resultStr


