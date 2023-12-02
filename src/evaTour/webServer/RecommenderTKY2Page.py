
from evaTour.webServer.BasicPage import getMenu
from evaTour.webServer.BasicPage import getTopbar
from evaTour.webServer.BasicPage import getFooter


def getRecommenderTKY2Page():
    return """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <title>Edukate - Online Education Website Template</title>
    <meta content="width=device-width, initial-scale=1.0" name="viewport">
    <meta content="Free HTML Templates" name="keywords">
    <meta content="Free HTML Templates" name="description">

    <!-- Favicon -->
    <link href="img/favicon.ico" rel="icon">

    <!-- Google Web Fonts -->
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Jost:wght@500;600;700&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet"> 

    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.10.0/css/all.min.css" rel="stylesheet">

    <!-- Libraries Stylesheet -->
    <link href="lib/owlcarousel/assets/owl.carousel.min.css" rel="stylesheet">
    
    <!-- Customized Bootstrap Stylesheet -->
    <link href="css/style.css" rel="stylesheet">

    <link rel = "stylesheet" href = "http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css"/>

<script>
    L.map("mapContainer").setView([37.7749, -122.4194], 13); //places the map in San Francisco.
</script>

</head>

<body>

""" + getTopbar() + """


""" + getMenu(3) + """


    <!-- Header Start -->
    <div class="jumbotron jumbotron-fluid page-header position-relative overlay-bottom" style="margin-bottom: 90px;">
        <div class="container text-center py-5">
            <h1 class="text-white display-1">Instructors</h1>
            <div class="d-inline-flex text-white mb-5">
                <p class="m-0 text-uppercase"><a class="text-white" href="">Home</a></p>
                <i class="fa fa-angle-double-right pt-1 px-3"></i>
                <p class="m-0 text-uppercase">Instructors</p>
            </div>
            <div class="mx-auto mb-5" style="width: 100%; max-width: 600px;">
                <div class="input-group">
                    <div class="input-group-prepend">
                        <button class="btn btn-outline-light bg-white text-body px-4 dropdown-toggle" type="button" data-toggle="dropdown"
                            aria-haspopup="true" aria-expanded="false">Courses</button>
                        <div class="dropdown-menu">
                            <a class="dropdown-item" href="#">Courses 1</a>
                            <a class="dropdown-item" href="#">Courses 2</a>
                            <a class="dropdown-item" href="#">Courses 3</a>
                        </div>
                    </div>
                    <input type="text" class="form-control border-light" style="padding: 30px 25px;" placeholder="Keyword">
                    <div class="input-group-append">
                        <button class="btn btn-secondary px-4 px-lg-5">Search</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Header End -->

    <!-- Team Start -->
    """ + getRecomLine("mapaL0") + """
    """ + getRecomLine("mapaL1") + """

    <!-- Team End -->


""" + getFooter() + """


    <!-- Back to Top -->
    <a href="#" class="btn btn-lg btn-primary rounded-0 btn-lg-square back-to-top"><i class="fa fa-angle-double-up"></i></a>


    <!-- JavaScript Libraries -->
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js"></script>
    <script src="lib/easing/easing.min.js"></script>
    <script src="lib/waypoints/waypoints.min.js"></script>
    <script src="lib/counterup/counterup.min.js"></script>
    <script src="lib/owlcarousel/owl.carousel.js"></script>

    <!-- Template Javascript -->
    <script src="js/main.js"></script>
	
</body>

</html>"""

def getRecomLine(mapName:str):
   resultStr:str = """
    <div class="container-fluid py-5">
        <div class="container py-5">
            <div class="owl-carousel team-carousel position-relative" style="padding: 0 30px;">
            """
   mapCount = 6
   for mapIDI in range(0,mapCount):
       mapNameAndMapIDI:str = mapName + str(mapIDI)
       resultStr += """
                <div class="team-item">
                    <script src = "http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>

                    <div id='"""+str(mapNameAndMapIDI)+"""' style="width:300px; height:300px; border:1px solid black"></div>
                    <style>
                        .main #mapid img{
                            border:none;
                            padding:0;
                            margin:0;
                        }
                    </style>
                    <script>
                        var latX =  -73.986909;
                        var latY =  40.736827;
                        var latMarkerX =  -73.986909;
                        var latMarkerY =  40.736827;
                        var markerText = "Hotel Uptown Palace 4*, Miláno - letecky, 3 dny";

                        var mymap = L.map('"""+str(mapNameAndMapIDI)+"""').setView([latY, latX], 10);

                        L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibHBlc2thIiwiYSI6ImNrYmx5dGh4cjA3MHMycW1pdHp4Y2ZheGoifQ.e-0fQLJYoUUxsM0X6Z-gxQ', {
                            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                            maxZoom: 18,
                            id: "mapbox/streets-v11",
                            tileSize: 512,
                            zoomOffset: -1,
                            accessToken: "pk.eyJ1IjoibHBlc2thIiwiYSI6ImNrYmx5dGh4cjA3MHMycW1pdHp4Y2ZheGoifQ.e-0fQLJYoUUxsM0X6Z-gxQ"
                        }).addTo(mymap);


                        var poly_line_6af745755bccf45d811207b88b49cc21 = L.polyline(
                            [[-73.986909, 40.736827], [-74.00417, 40.738098], [-74.00347624542094, 40.73616151907358], [-74.00300568511572, 40.733101548455984]],
                            {"bubblingMouseEvents": true, "color": "#8EE9FF", "dashArray": null, "dashOffset": null, "fill": false, "fillColor": "#8EE9FF", "fillOpacity": 0.2, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1.0, "smoothFactor": 1.0, "stroke": true, "weight": 15}
                        ).addTo(mymap);

                    </script>
                    <div class="bg-light text-center p-4">
                        <h5 class="mb-3">Instructor """+str(mapIDI)+"""</h5>
                        <p class="mb-2">Web Design & Development</p>
                        <div class="d-flex justify-content-center">
                            <a class="mx-1 p-1" href="#"><i class="fab fa-twitter"></i></a>
                            <a class="mx-1 p-1" href="#"><i class="fab fa-facebook-f"></i></a>
                            <a class="mx-1 p-1" href="#"><i class="fab fa-linkedin-in"></i></a>
                            <a class="mx-1 p-1" href="#"><i class="fab fa-instagram"></i></a>
                            <a class="mx-1 p-1" href="#"><i class="fab fa-youtube"></i></a>
                        </div>
                    </div>
                </div>
                """
   resultStr += """
            </div>
        </div>
    </div>
"""
   print(resultStr)
   return resultStr

def getRecomLine0(mapName:str):
   resultStr:str = """
    <div class="container-fluid py-5">
        <div class="container py-5">
            <div class="owl-carousel team-carousel position-relative" style="padding: 0 30px;">
            """
   mapCount = 6
   for mapIDI in range(0,mapCount):
       mapNameAndMapIDI:str = mapName + str(mapIDI)
       resultStr += """
                <div class="team-item">
                    <script src = "http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>

                    <iframe width="400" height="300" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"
                        src="https://www.openstreetmap.org/export/embed.html?bbox=-62.04673002474011%2C16.95487694424327%2C-61.60521696321666%2C17.196751341562923&amp; marker=-61.99504948648988%2C16.953157460689545; layer=mapnik"
                        style="border: 1px solid black">
                    </iframe>

                    <br/><small><a href="https://www.openstreetmap.org/#map=12/17.0759/-61.8260">View Larger Map</a></small>

                    <script>
                    </script>
                    <div class="bg-light text-center p-4">
                        <h5 class="mb-3">Instructor """+str(mapIDI)+"""</h5>
                        <p class="mb-2">Web Design & Development</p>
                        <div class="d-flex justify-content-center">
                            <a class="mx-1 p-1" href="#"><i class="fab fa-twitter"></i></a>
                            <a class="mx-1 p-1" href="#"><i class="fab fa-facebook-f"></i></a>
                            <a class="mx-1 p-1" href="#"><i class="fab fa-linkedin-in"></i></a>
                            <a class="mx-1 p-1" href="#"><i class="fab fa-instagram"></i></a>
                            <a class="mx-1 p-1" href="#"><i class="fab fa-youtube"></i></a>
                        </div>
                    </div>
                </div>
                """
   resultStr += """
            </div>
        </div>
    </div>
"""
   print(resultStr)
   return resultStr

def getRecomLine1(mapName:str):
   resultStr:str = """
    <div class="container-fluid py-5">
        <div class="container py-5">
            <div class="owl-carousel team-carousel position-relative" style="padding: 0 30px;">
            """
   mapCount = 6
   for mapIDI in range(0,mapCount):
       mapNameAndMapIDI:str = mapName + str(mapIDI) 
       resultStr += """
                <div class="team-item">
                    <div id='"""+str(mapNameAndMapIDI)+"""' style="width:300px; height:300px; border:1px solid black"></div>
                    <script src = "http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>
                    <script>

              var latX =  17.7816896;
              var latY =  49.1379062;
              var latMarkerX =  17.7816896;
              var latMarkerY =  49.1379062;

                         var mymap"""+str(mapNameAndMapIDI)+""" = L.map('"""+str(mapNameAndMapIDI)+"""').setView([latY, latX], 10);
                         L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibHBlc2thIiwiYSI6ImNrYmx5dGh4cjA3MHMycW1pdHp4Y2ZheGoifQ.e-0fQLJYoUUxsM0X6Z-gxQ', {
                            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                            maxZoom: 18,
                            id: "mapbox/streets-v11",
                            tileSize: 512,
                            zoomOffset: -1,
                            accessToken: "pk.eyJ1IjoibHBlc2thIiwiYSI6ImNrYmx5dGh4cjA3MHMycW1pdHp4Y2ZheGoifQ.e-0fQLJYoUUxsM0X6Z-gxQ"
                         }).addTo(mymap"""+str(mapNameAndMapIDI)+""");

                        var marker2 = L.marker([latMarkerY,latMarkerX]).addTo(mymap);
                        marker2.bindPopup(markerText);

                    </script>
                    <div class="bg-light text-center p-4">
                        <h5 class="mb-3">Instructor """+str(mapIDI)+"""</h5>
                        <p class="mb-2">Web Design & Development</p>
                        <div class="d-flex justify-content-center">
                            <a class="mx-1 p-1" href="#"><i class="fab fa-twitter"></i></a>
                            <a class="mx-1 p-1" href="#"><i class="fab fa-facebook-f"></i></a>
                            <a class="mx-1 p-1" href="#"><i class="fab fa-linkedin-in"></i></a>
                            <a class="mx-1 p-1" href="#"><i class="fab fa-instagram"></i></a>
                            <a class="mx-1 p-1" href="#"><i class="fab fa-youtube"></i></a>
                        </div>
                    </div>
                </div>
                """
   resultStr += """
            </div>
        </div>
    </div>
"""
   print(resultStr)
   return resultStr



def getRecomLine2(mapName:str):
   resultStr:str = """
    <div class="container-fluid py-5">
        <div class="container py-5">
            <div class="owl-carousel team-carousel position-relative" style="padding: 0 30px;">
            """
   mapCount = 6
   for mapIDI in range(0,mapCount):
       mapNameAndMapIDI:str = mapName + str(mapIDI)
       resultStr += """
                <div class="team-item">
                    <div id='"""+str(mapNameAndMapIDI)+"""' style="width:300px; height:300px; border:1px solid black"></div>
                    <script src = "http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>
                    <script>
                         // Creating map options
                         var mapOptions"""+str(mapNameAndMapIDI)+""" = {
                            center: [17.385044, 78.486671],
                            zoom: 10
                         }

                         // Creating a map object
                         var map"""+str(mapNameAndMapIDI)+""" = new L.map('"""+str(mapNameAndMapIDI)+"""', mapOptions"""+str(mapNameAndMapIDI)+""");

                         // Creating a Layer object
                         var layer"""+str(mapNameAndMapIDI)+""" = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');

                         // Adding layer to the map
                         map"""+str(mapNameAndMapIDI)+""".addLayer(layer"""+str(mapNameAndMapIDI)+""");
                         map"""+str(mapNameAndMapIDI)+""".invalidateSize(false)

                    </script>
                    <div class="bg-light text-center p-4">
                        <h5 class="mb-3">Instructor """+str(mapIDI)+"""</h5>
                        <p class="mb-2">Web Design & Development</p>
                        <div class="d-flex justify-content-center">
                            <a class="mx-1 p-1" href="#"><i class="fab fa-twitter"></i></a>
                            <a class="mx-1 p-1" href="#"><i class="fab fa-facebook-f"></i></a>
                            <a class="mx-1 p-1" href="#"><i class="fab fa-linkedin-in"></i></a>
                            <a class="mx-1 p-1" href="#"><i class="fab fa-instagram"></i></a>
                            <a class="mx-1 p-1" href="#"><i class="fab fa-youtube"></i></a>
                        </div>
                    </div>
                </div>
                """
   resultStr += """
            </div>
        </div>
    </div>
"""
   #print(resultStr)
   return resultStr
