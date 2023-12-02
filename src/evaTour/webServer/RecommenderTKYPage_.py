
from evaTour.webServer.BasicPage import getMenu
from evaTour.webServer.BasicPage import getTopbar
from evaTour.webServer.BasicPage import getFooter


def getRecommenderTKYPage():
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
    
    <script src="https://api.mapy.cz/loader.js"></script>
    <script>Loader.load()</script>

<script>
    function move(){
        //do something on mouse move
        document.getElementById("mapaL01").invalidateSize();
        document.getElementById("mapaL02").invalidateSize();
        document.getElementById("mapaL03").invalidateSize();
        document.getElementById("mapaL04").invalidateSize();
        //alert('aaa')
        //alert(elem)

    }

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
                <div id='"""+str(mapNameAndMapIDI)+"""' style="width:300px; height:300px;"></div>
	                <script type="text/javascript">		               
		               var center = SMap.Coords.fromWGS84(14.41790, 50.12655);
                       var """+str(mapNameAndMapIDI)+""" = new SMap(JAK.gel('"""+str(mapNameAndMapIDI)+"""'), center, 13);
                       """+str(mapNameAndMapIDI)+""".addControl(new SMap.Control.Sync()); /* Aby mapa reagovala na změnu velikosti průhledu */
                       """+str(mapNameAndMapIDI)+""".addDefaultLayer(SMap.DEF_TURIST).enable(); /* Turistický podklad */

                       var mouse"""+str(mapNameAndMapIDI)+""" = new SMap.Control.Mouse(SMap.MOUSE_PAN | SMap.MOUSE_WHEEL | SMap.MOUSE_ZOOM); /* Ovládání myší */
                       """+str(mapNameAndMapIDI)+""".addControl(mouse"""+str(mapNameAndMapIDI)+""");

                       var xhr"""+str(mapNameAndMapIDI)+""" = new JAK.Request(JAK.Request.XML);
                       xhr"""+str(mapNameAndMapIDI)+""".setCallback(window, "response"""+str(mapNameAndMapIDI)+"""");
                       xhr"""+str(mapNameAndMapIDI)+""".send("api.mapy.cz/xml/sample.xml");

                      var response"""+str(mapNameAndMapIDI)+""" = function(xmlDoc) {
                          var gpx"""+str(mapNameAndMapIDI)+""" = new SMap.Layer.GPX(xmlDoc);
                          """+str(mapNameAndMapIDI)+""".addLayer(gpx"""+str(mapNameAndMapIDI)+""");
                          """+str(mapNameAndMapIDI)+""".redraw()
                          gpx"""+str(mapNameAndMapIDI)+""".enable();
                          gpx"""+str(mapNameAndMapIDI)+""".fit();
                     }   
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
    <!-- <button onclick="fun()">What is the time?</button> -->
    <button onclick="fun()">What is the time?</button>
"""
   print(resultStr)
   return resultStr
