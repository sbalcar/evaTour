
from evaTour.webServer.BasicPage import getMenu
from evaTour.webServer.BasicPage import getTopbar
from evaTour.webServer.BasicPage import getFooter
from evaTour.webServer.BasicComponents import getNYCCounters
from evaTour.webServer.BasicComponents import getTKYCounters

def getDataPage():
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
</head>

<body>

""" + getTopbar() + """


""" + getMenu(2) + """


    <!-- Header Start -->
    <div class="jumbotron jumbotron-fluid page-header position-relative overlay-bottom" style="margin-bottom: 90px;">
        <div class="container text-center py-5">
            <h1 class="text-white display-1">Data</h1>
            <div class="d-inline-flex text-white mb-5">
                <p class="m-0 text-uppercase"><a class="text-white" href="">Home</a></p>
                <i class="fa fa-angle-double-right pt-1 px-3"></i>
                <p class="m-0 text-uppercase">Data</p>
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

    <div class="container-fluid px-0 py-5">
        <div class="row mx-0 justify-content-center pt-5">
            <div class="col-lg-6">
                     <div class="section-title text-center position-relative mb-4">
                        <h1 class="display-4">FourSquare datasets</h1>
                    </div>

                     <p>Project is based on  FourSquare <a href='https://sites.google.com/site/yangdingqi/home/foursquare-dataset'> NYC and Tokyo Check-in Datset </a>. This dataset allows us to overcome cold-start-problem.</p>
                     
                     <p>Data were filtered. We removed e.g. Restaurants, Miscellaneous shops, Post Offices, Public transit stops. There was used these 66 distinguishable venue categories:</p>
                     <p>['Castle', 'Arcade', 'Pool', 'Public Art', 'Museum', 'Harbor / Marina', 'Zoo', 'Outdoors & Recreation', 'General Entertainment', 'Other Great Outdoors', 'River', 'Aquarium', 'Plaza', 'Library', 'Art Museum', 'Beach', 'Synagogue', 'Spa / Massage', 'Theater', 'Concert Hall', 'Event Space', 'Temple', 'Church', 'Garden', 'Performing Arts Venue', 'Shrine', 'Historic Site', 'Convention Center', 'Brewery', 'History Museum', 'Cemetery', 'Science Museum', 'Park', 'Scenic Lookout', 'Mosque', 'Pool Hall', 'Art Gallery', 'Building', 'Arts & Entertainment', 'Planetarium', 'Movie Theater', 'Campground', 'Sculpture Garden', 'Bridge']</p>
                     
                     <p>As the metric of distances we use Euclidean distance precomputed from GPS coordinates.</p>

                     <div class="section-title text-center position-relative mb-4">
                        <h3>NYC FourSquare filtred dataset</h1>
                     
""" + getNYCCounters() + """
                    </div>

                     <div class="section-title text-center position-relative mb-4">
                        <h3>TKY FourSquare filtred dataset</h1>

""" + getTKYCounters() + """
                      </div>

            </div>
         </div>
     </div>

""" + getFooter() + """



    <!-- Back to Top -->
    <a href="#" class="btn btn-lg btn-primary rounded-0 btn-lg-square back-to-top"><i class="fa fa-angle-double-up"></i></a>


    <!-- JavaScript Libraries -->
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js"></script>
    <script src="lib/easing/easing.min.js"></script>
    <script src="lib/waypoints/waypoints.min.js"></script>
    <script src="lib/counterup/counterup.min.js"></script>
    <script src="lib/owlcarousel/owl.carousel.min.js"></script>

    <!-- Template Javascript -->
    <script src="js/main.js"></script>
</body>

</html>"""
