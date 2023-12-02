import cherrypy

def getTopbar():
    isLogined:bool = cherrypy.session.get('username') != None
    print("isLogined: " + str(isLogined))

    result = """
    <!-- Topbar Start -->
    <div class="container-fluid bg-dark">
        <div class="row py-2 px-lg-5">
            <div class="col-lg-6 text-center text-lg-left mb-2 mb-lg-0">
                <div class="d-inline-flex align-items-center text-white">
                    <small><i class="fa fa-phone-alt mr-2"></i>+420  95155 4250</small>
                    <small class="px-3">|</small>
                    <small><i class="fa fa-envelope mr-2"></i>ksi@mff.cuni.cz</small>
                </div>"""
    if isLogined:
        result += """
                <div class="d-inline-flex align-items-center text-white">
                    <small style="padding: 0px 150px;">Login: """ +  cherrypy.session.get('username') + """</small>
                </div>"""
    result += """
            </div>
            <div class="col-lg-6 text-center text-lg-right">
                <div class="d-inline-flex align-items-center">
                    <a class="text-white px-2" href="">
                        <i class="fab fa-facebook-f"></i>
                    </a>
                    <a class="text-white px-2" href="">
                        <i class="fab fa-twitter"></i>
                    </a>
                    <a class="text-white px-2" href="">
                        <i class="fab fa-linkedin-in"></i>
                    </a>
                    <a class="text-white px-2" href="">
                        <i class="fab fa-instagram"></i>
                    </a>
                    <a class="text-white pl-2" href="">
                        <i class="fab fa-youtube"></i>
                    </a>
                </div>
            </div>
        </div>
    </div>
    <!-- Topbar End -->
"""
    return result

def getMenu(selectedMenuItem:int):
   active0, active1, active2, active3, active4, active5 = "", "", "", "", "", ""
   if  selectedMenuItem == 0:
       active0 = 'active'
   if  selectedMenuItem == 1:
       active1 = 'active'
   if  selectedMenuItem == 2:
       active2 = 'active'
   if  selectedMenuItem == 3:
       active3 = 'active'
   if  selectedMenuItem == 4:
       active4 = 'active'
   if  selectedMenuItem == 5:
       active5 = 'active'

   #print(type(cherrypy.session))
   isLogined:bool = cherrypy.session.get('username') != None

   result = """
    <!-- Navbar Start -->
    <div class="container-fluid p-0">
        <nav class="navbar navbar-expand-lg bg-white navbar-light py-3 py-lg-0 px-lg-5">
            <a href="index" class="navbar-brand ml-lg-3">
                <h1 class="m-0 text-uppercase text-primary"><i class="fa fa-book-reader mr-3"></i>Evatour</h1>
            </a>
            <button type="button" class="navbar-toggler" data-toggle="collapse" data-target="#navbarCollapse">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-between px-lg-3" id="navbarCollapse">
                <div class="navbar-nav mx-auto py-0">
                    <a href="index" class="nav-item nav-link """ + active0 + """">Home</a>
                    <a href="contribution" class="nav-item nav-link """ + active1 + """">Contribution</a>
                    <a href="data" class="nav-item nav-link """ + active2 + """">Data</a>
                    <div class="nav-item dropdown">
                        <a href="#" class="nav-link dropdown-toggle  """ + active3 + """" data-toggle="dropdown">Recommenders</a>
                        <div class="dropdown-menu m-0">
                            <a href="recommender_nyc" class="dropdown-item">RS NYC1</a>
                             <a href="recommender_nyc2" class="dropdown-item">RS NYC2</a>
                            <a href="recommender_tky" class="dropdown-item">RS TKY1</a>
                            <a href="recommender_tky2" class="dropdown-item">RS TKY2</a>
                        </div>
                    </div>
                    <a href="teams" class="nav-item nav-link """ + active4 + """">Teams</a>
                    <a href="contact" class="nav-item nav-link """ + active5 + """">Contact</a>
                </div>"""
   if isLogined:
       result += """
                <a href="log_out" class="btn btn-primary py-2 px-4 d-none d-lg-block">Log out</a>"""
   else:
       result += """
                <a href="log_in" class="btn btn-primary py-2 px-4 d-none d-lg-block">Join Us</a>"""

   result += """
            </div>
        </nav>
    </div>
    <!-- Navbar End -->
"""
   return result


def getFooter():
   return """
    <!-- Footer Start -->
    <div class="container-fluid position-relative overlay-top bg-dark text-white-50 py-5" style="margin-top: 90px;">
        <div class="container mt-5 pt-5">
            <div class="row">
                <div class="col-md-6 mb-5">
                    <a href="index.html" class="navbar-brand">
                        <h1 class="mt-n2 text-uppercase text-white"><i class="fa fa-book-reader mr-3"></i>Evatour</h1>
                    </a>
                    <p class="m-0">Project is developed at Charles University, Faculty of Mathematics and Physics, by Department of Software Engineering.</p>
                </div>
                <div class="col-md-6 mb-5">
                    <h3 class="text-white mb-4">Newsletter</h3>
                    <div class="w-100">
                        <div class="input-group">
                            <input type="text" class="form-control border-light" style="padding: 30px;" placeholder="Your Email Address">
                            <div class="input-group-append">
                                <button class="btn btn-primary px-4">Sign Up</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-4 mb-5">
                    <h3 class="text-white mb-4">Get In Touch</h3>
                    <p><i class="fa fa-map-marker-alt mr-2"></i>Malostranské náměstí 25,| 118 00, Praha 1</p>
                    <p><i class="fa fa-phone-alt mr-2"></i>+420 951 554250</p>
                    <p><i class="fa fa-envelope mr-2"></i>ksi@mff.cuni.cz</p>
                    <div class="d-flex justify-content-start mt-4">
                        <a class="text-white mr-4" href="#"><i class="fab fa-2x fa-twitter"></i></a>
                        <a class="text-white mr-4" href="#"><i class="fab fa-2x fa-facebook-f"></i></a>
                        <a class="text-white mr-4" href="#"><i class="fab fa-2x fa-linkedin-in"></i></a>
                        <a class="text-white" href="#"><i class="fab fa-2x fa-instagram"></i></a>
                    </div>
                </div>
                <div class="col-md-4 mb-5">
                    <h3 class="text-white mb-4">Our Courses</h3>
                    <div class="d-flex flex-column justify-content-start">
                        <a class="text-white-50 mb-2" href="#"><i class="fa fa-angle-right mr-2"></i>Web Design</a>
                        <a class="text-white-50 mb-2" href="#"><i class="fa fa-angle-right mr-2"></i>Apps Design</a>
                        <a class="text-white-50 mb-2" href="#"><i class="fa fa-angle-right mr-2"></i>Marketing</a>
                        <a class="text-white-50 mb-2" href="#"><i class="fa fa-angle-right mr-2"></i>Research</a>
                        <a class="text-white-50" href="#"><i class="fa fa-angle-right mr-2"></i>SEO</a>
                    </div>
                </div>
                <div class="col-md-4 mb-5">
                    <h3 class="text-white mb-4">Quick Links</h3>
                    <div class="d-flex flex-column justify-content-start">
                        <a class="text-white-50 mb-2" href="#"><i class="fa fa-angle-right mr-2"></i>Privacy Policy</a>
                        <a class="text-white-50 mb-2" href="#"><i class="fa fa-angle-right mr-2"></i>Terms & Condition</a>
                        <a class="text-white-50 mb-2" href="#"><i class="fa fa-angle-right mr-2"></i>Regular FAQs</a>
                        <a class="text-white-50 mb-2" href="#"><i class="fa fa-angle-right mr-2"></i>Help & Support</a>
                        <a class="text-white-50" href="#"><i class="fa fa-angle-right mr-2"></i>Contact</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="container-fluid bg-dark text-white-50 border-top py-4" style="border-color: rgba(256, 256, 256, .1) !important;">
        <div class="container">
            <div class="row">
                <div class="col-md-6 text-center text-md-left mb-3 mb-md-0">
                    <p class="m-0">Copyright &copy; <a class="text-white" href="#">Your Site Name</a>. All Rights Reserved.
                    </p>
                </div>
                <div class="col-md-6 text-center text-md-right">
                    <p class="m-0">Designed by <a class="text-white" href="https://htmlcodex.com">HTML Codex</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
    <!-- Footer End -->
"""