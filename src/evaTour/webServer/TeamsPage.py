from evaTour.datasets.usersSimilarity import userSimilarity
from evaTour.webServer.BasicPage import getMenu
from evaTour.webServer.BasicPage import getTopbar
from evaTour.webServer.BasicPage import getFooter
from evaTour.webServer.datamodels.UsersModel import UsersModel
from evaTour.webServer.datamodels.TeamsModel import TeamsModel

from typing import List


def getTeamsPage(userId:int, teamsModel:TeamsModel, usersModel:UsersModel, similarityDFNYC, similarityDFTKY, selTeamID=None):
   containsError = False
   resultStr = """<!DOCTYPE html>
<html lang="en">
0
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


""" + getMenu(4) + """


    <!-- Header Start -->
    <div class="jumbotron jumbotron-fluid page-header position-relative overlay-bottom" style="margin-bottom: 90px;">
        <div class="container text-center py-5">
            <h1 class="text-white display-1">Teams</h1>
            <div class="d-inline-flex text-white mb-5">
                <p class="m-0 text-uppercase"><a class="text-white" href="">Home</a></p>
                <i class="fa fa-angle-double-right pt-1 px-3"></i>
                <p class="m-0 text-uppercase">Teams</p>
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




    <!-- Users Start -->
    <div class="container-fluid px-0 py-5">
        <div class="row mx-0 justify-content-center pt-5">
            <div class="col-lg-6">
                     <div class="section-title text-center position-relative mb-4">
                        <h1 class="display-4">My teams</h1>
                     </div>
                        <div class="d-flex align-items-center mb-5">

                           <table border = "1">
                             <tr bgcolor="2d7de8">
                               <th style="color:white;text-align:center;vertical-align:middle">Team ID</th>
                               <th style="color:white;text-align:center;vertical-align:middle">Team Name</th>
                               <th style="color:white;text-align:center;vertical-align:middle">Destinations</th>
                               <th style="color:white;text-align:center;vertical-align:middle">Members</th>
                               <th style="color:white;text-align:center;vertical-align:middle">Remove team</th>
                               <th style="color:white;text-align:center;vertical-align:middle">Mark team</th>
                               <th style="color:white;text-align:center;vertical-align:middle">Recommend</th>
                             </tr>"""
   for rawI in teamsModel._modelDF.itertuples():
      teamIdI = rawI[1]
      teamNameI = rawI[2]
      destinationsI = rawI[3]
      membersI = rawI[4]

      selTrAppendix = ""
      selTdAppendix = ""
      selButtonLabel = "Select"
      selButtonValueOfTeamId = teamIdI
      if selTeamID != None and selTeamID != "None":
         if int(teamIdI) == int(selTeamID):
            selTrAppendix = "bgcolor = 'f55d61'"
            selTdAppendix = "style='color:white;text-align:center;vertical-align:middle'"
            selButtonLabel = "Deselect"
            selButtonValueOfTeamId = None

      resultStr += """
                             <tr """ + str(selTrAppendix) + """>
                               <td """ + str(selTdAppendix) + """>""" + str(teamIdI) + """</td>
                               <td """ + str(selTdAppendix) + """>""" + str(teamNameI) + """</td>
                               <td """ + str(selTdAppendix) + """>""" + str(destinationsI) + """</td>
                               <td """ + str(selTdAppendix) + """>""" + str(membersI) + """</td>
                               <td """ + str(selTdAppendix) + """>
                                   <form action="/team_delete" method="get"><button class="btn btn-primary py-3 px-5" type="submit">Remove</button>
                                         <input type="hidden" name="teamID" value='""" + str(teamIdI) +  """'/>
                                   </form></td>
                               <td """ + str(selTdAppendix) + """>
                                   <form action="/teams" method="get"><button class="btn btn-primary py-3 px-5" type="submit" style="width:100%">""" + str(selButtonLabel) + """</button>
                                         <input type="hidden" name="selTeamID" value='""" + str(selButtonValueOfTeamId) +  """'/>
                                   </form></td>
                               <td """ + str(selTdAppendix) + """>
                                   <form action="/group_recommender" method="get"><button class="btn btn-primary py-3 px-5" type="submit">Recommend for team</button>
                                         <input type="hidden" name="teamID" value='""" + str(teamIdI) +  """'/>
                                   </form></td>
                             </tr>
                             """
   resultStr += """   
                           </table>
                        </div>
                     </div>
            </div>
        </div>
    </div>
    <!-- Users End -->





     
     
     <div class="container-fluid px-0 py-5">
        <div class="row justify-content-center bg-image mx-0 mb-5">
            <div class="col-lg-6 py-5">
                <div class="bg-white p-5 my-5">
                    <h3 class="text-center mb-4">Add new team</h3>

                    <form method="post" action="/team_add">
                        <div class="form-row">
                            <div class="col-sm-6">
                                <div class="form-group">
                                    <input type="text" class="form-control bg-light border-0" name="teamName" placeholder='Wanderers Team' style="padding: 20px 20px;">
                                </div>
                            </div>
                            <div class="col-sm-6">
                                <div class="form-group">
                                    <select class="form-control bg-light border-0" name="destination">
                                      <option value="NYC">New York City</option>
                                      <option value="TKY">Tokyo City</option>
                                    </select>
                                </div>
                            </div>
                            <input type="hidden" name="userID" value='""" + str(userId) +  """'/>
                            <div class="col-sm-6">
                                <div class="form-group">
                                    <button class="btn btn-primary btn-block" type="submit" style="height: 40px;">Add the New Team Now</button>
                                </div>
                            </div>
                            """
   if containsError:
      resultStr += """
                            <div class="col-sm-6">
                                <div class="form-group" style="padding: 20px 30px;">
                                    <h5 style="color:red;">Login name or password is incorrect.<h5/>
                                </div>
                            </div>"""
   resultStr += """
                        </div>
                    </form>

                </div>
            </div>
        </div>
     </div>

     
     


    <!-- Users Start -->
    <div class="container-fluid px-0 py-5">
        <div class="row mx-0 justify-content-center pt-5">
            <div class="col-lg-6">
                     <div class="section-title text-center position-relative mb-4">
                        <h1 class="display-4">Other Users</h1>
                     </div>
                        <div class="d-flex align-items-center mb-5">

                           <table border = "1">
                             <tr bgcolor="2d7de8">
                               <th style="color:white;text-align:center;vertical-align:middle">User ID</th>
                               <th style="color:white;text-align:center;vertical-align:middle">Login</th>
                               <th style="color:white;text-align:center;vertical-align:middle">Detail</th>
                               <th style="color:white;text-align:center;vertical-align:middle">Destinations</th>
                               <th style="color:white;text-align:center;vertical-align:middle">Similarity</th>
                               <th style="color:white;text-align:center;vertical-align:middle">Team</th>
                             </tr>"""
   for rawI in usersModel._modelDF.itertuples():
      userIDI = int(rawI[2])
      loginI = rawI[3]
      destinationI = rawI[4]
      similarityI = userSimilarity(userId, userIDI, similarityDFNYC, similarityDFTKY)
      isMember = False
      if selTeamID != None:
         isMember = teamsModel.isMember(userIDI, int(selTeamID))
      resultStr += """   
                             <tr>
                               <td>""" + str(userIDI) + """</td>
                               <td>""" + str(loginI) + """</td>
                               <td><form action="/user_detail" method="get"><button class="btn btn-primary py-3 px-5" type="submit">Detail</button>
                                         <input type="hidden" name="userID" value='""" + str(userIDI) +  """'/>
                                   </form></td>
                               <td>""" + str(destinationI) + """</td>
                               <td>""" + str(similarityI) + """</td>"""
      if isMember:
         resultStr += """
                               <td><form action="/team_del_user" method="get"><button class="btn btn-primary py-3 px-5" type="submit" style="width:100%">Remove</button>
                                         <input type="hidden" name="userID" value='""" + str(userIDI) + """'/>
                                         <input type="hidden" name="teamID" value='""" + str(selTeamID) + """'/>

                                   </form></td>"""
      else:
         resultStr += """
                               <td><form action="/team_add_new_user" method="get"><button class="btn btn-primary py-3 px-5" type="submit" style="width:100%">Add to my team</button>
                                         <input type="hidden" name="userID" value='""" + str(userIDI) +  """'/>
                                         <input type="hidden" name="teamID" value='""" + str(selTeamID) +  """'/>
                                         
                                   </form></td>"""
   resultStr += """
                             </tr>
                           </table>
                        </div>
                     </div>
            </div>
        </div>
    </div>
    <!-- Users End -->


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
   return resultStr