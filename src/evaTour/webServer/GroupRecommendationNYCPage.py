from evaTour.ea.eaislandmodel.islandModel import IslandModel
from evaTour.ea.eaislandmodel.islandEATabu import IslandEATabu
from evaTour.ea.operatorRTMigration import migrationTabu
from evaTour.recommenders.recommenderSVDS import RecommenderSVDS
from evaTour.webServer.BasicPage import getMenu
from evaTour.webServer.BasicPage import getTopbar
from evaTour.webServer.BasicPage import getFooter

from evaTour.maps.openStreetMaps import convertIndividualToGPS

from evaTour.ea.operators.roundtrip.generator.generatorRtRoulette import GeneratorRtRoulette
from evaTour.ea.operators.roundtrip.fitness.fitnessKmPrecalculatedTSP import FitnessKmPrecalculatedTSP
from evaTour.ea.operators.selectionGeneral.selectionRoulette import SelectionRoulette

from evaTour.ea.operators.roundtrip.crossover.crossoverRtPMX import CrossoverRtPMX
from evaTour.ea.operators.roundtrip.mutation.mutationRt2Opt import MutationRt2Opt

from evaTour.webServer.datamodels.UsersModel import UsersModel
from evaTour.webServer.datamodels.TeamsModel import TeamsModel

from pandas import Series
from typing import List
from pandas import DataFrame

import cherrypy


def getGroupRecommenderPage(userIDI:int, teamID:int, userModel:UsersModel, teamsModel:TeamsModel,
                            r:RecommenderSVDS, ratingsDF:DataFrame, itemsDF:DataFrame, distancesDF:DataFrame):

    userIDsMembers:List = teamsModel.getUserIDsOfTeam(teamID)
    print("userIDsMembers: " + str(userIDsMembers))

    for userIdI in userIDsMembers:
        print("userIdI: " + str(userIdI))
        transUserIdI = userModel.translateUserIdToDatasetUserId(int(userIdI))
        print("transUserIdI: " + str(transUserIdI))
        recomI = r.recommend(transUserIdI, 50)
        print("recomI: " + str(recomI))

    individual = list(range(20, 50))

    fitnessValue = FitnessKmPrecalculatedTSP(itemsDF, distancesDF).run(individual)
    print("FitnessValue: " + str(fitnessValue))
    print("")

    uIdI = 1
    n_bits = 20
    iterCount = 200
    popSize = 20
    crossRate = 0.5
    mutRate = 0.2
    numberOfIslands = 8
    roundtripLength = 15


    recommendation:Series = r.recommend(uIdI, 200)
    itemIDs:List = list(recommendation.keys())
    scores:List = list(recommendation.values)

    islands:List = []
    for islandNumberI in range(numberOfIslands):
        eI = IslandEATabu(islandNumberI)
        eI.setPopGeneratorFnc(GeneratorRtRoulette(roundtripLength, itemIDs, scores))
        eI.setFitnessFnc(FitnessKmPrecalculatedTSP(itemsDF, distancesDF))
        eI.setSelectionFnc(SelectionRoulette())
        eI.setCrossoverFnc(CrossoverRtPMX())
        eI.setMutationFnc(MutationRt2Opt())

        islands.append(eI)

    eim = IslandModel(islands)
    eim.setMigrationFnc(migrationTabu, {IslandEATabu.ARG_MIGRATION_GEN_PERIOD:10})
    eim.run(iterCount, popSize, crossRate, mutRate)

    indivDict = {}
    indivGPSDict = {}
    fitnessDict = {}
    for i in range(len(eim.resultBestIndivDict.values())):
        indivI = eim.resultBestIndivDict.values()[i]
        #print("indivI: " + str(indivI))
        indivGPSI = convertIndividualToGPS(indivI, itemsDF)
        fitnessI = eim.resultBestFitnessDict.values()[i]

        indivDict[i] = indivI
        indivGPSDict[i] = indivGPSI
        fitnessDict[i] = fitnessI

    cherrypy.session['indivDict'] = indivDict
    cherrypy.session['indivGPSDict'] = indivGPSDict
    cherrypy.session['fitnessDict'] = fitnessDict

    shortLength = 15
    mediumLength = 30
    longLength = 50

    title0:str = "Short (" + str(shortLength) + ") touristic roundtrip"
    title1:str = "Medium (" + str(mediumLength) + ") touristic roundtrip"
    title2:str = "Long (" + str(longLength) + ") touristic roundtrip"

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

</head>

<body>

""" + getTopbar() + """


""" + getMenu(3) + """


    <!-- Header Start -->
    <div class="jumbotron jumbotron-fluid page-header position-relative overlay-bottom" style="margin-bottom: 90px;">
        <div class="container text-center py-5">
            <h3 class="text-white display-1">Recommender NYC</h3>
            <div class="d-inline-flex text-white mb-5">
                <p class="m-0 text-uppercase"><a class="text-white" href="">Home</a></p>
                <i class="fa fa-angle-double-right pt-1 px-3"></i>
                <p class="m-0 text-uppercase">Recommender NYC</p>
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
    """ + getRecomLine(0, title0) + """
    """ + getRecomLine(1, title1) + """
    """ + getRecomLine(2, title2) + """
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


def getRecomLine(row:int, title:str):
    resultStr: str = """
    <div class="container-fluid py-5">
        <div class="container py-5">
            <div class="section-title text-center position-relative mb-4">
                <h1 class="display-4">""" + title + """</h1>
             </div>
            <div class="owl-carousel team-carousel position-relative" style="padding: 0 30px;">
            """
    mapCount = 6
    for colIDI in range(0, mapCount):
        fitnessStrI = str(cherrypy.session['fitnessDict'][colIDI])
        resultStr += """
                <div class="team-item">

                    <iframe width="400" height="400" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"
                        src="/mapOSM?row=""" + str(row) + """;column=""" + str(colIDI) + """" 
                        style="border: 1px solid black">
                    </iframe>

                    <br/><small><a href="/mapOSM?row=""" + str(row) + """;column=""" + str(colIDI) + """">View Larger Map</a></small>

                    <div class="bg-light text-center p-4">
                        <h5 class="mb-3">Indiv: """ + str(colIDI) + """</h5>
                        <p class="mb-2">Fitness: """ + fitnessStrI + """ Km</p>
                    """
                        #<p class="mb-2">""" + str(cherrypy.session['indivDict'][colIDI]) + """ </p>

        resultStr += """
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
