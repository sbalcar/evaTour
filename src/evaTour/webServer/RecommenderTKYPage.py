from evaTour.webServer.BasicPage import getMenu
from evaTour.webServer.BasicPage import getTopbar
from evaTour.webServer.BasicPage import getFooter

from evaTour.maps.openStreetMaps import convertIndividualToGPS

from evaTour.ea.easimple.ea import EvolutionAlgorithm
from evaTour.ea.operators.roundtrip.generator.generatorRtPerm import GeneratorRtPerm
from evaTour.ea.operators.roundtrip.fitness.fitnessKmPrecalculatedTSP import FitnessKmPrecalculatedTSP
from evaTour.ea.operators.selectionGeneral.selectionRoulette import SelectionRoulette

from evaTour.ea.operators.roundtrip.crossover.crossoverRtPMX import CrossoverRtPMX
from evaTour.ea.operators.roundtrip.mutation.mutationRt2Opt import MutationRt2Opt

from typing import List
from pandas import DataFrame

import cherrypy


def getRecommenderTKYPage(ratingsDF:DataFrame, itemsDF:DataFrame, distancesDF:DataFrame):

    individual = list(range(20,50))

    fitnessValue = FitnessKmPrecalculatedTSP(itemsDF, distancesDF).run(individual)
    print("FitnessValue: " + str(fitnessValue))
    print("")

    iterCount = 200
    popSize = 20
    crossRate = 0.5
    mutRate = 0.5

    e = EvolutionAlgorithm()
    e.setIterCount(iterCount)
    e.setPopSize(popSize)
    e.setCrossRate(crossRate)
    e.setMutRate(mutRate)
    e.setPopGeneratorOpr(GeneratorRtPerm(individual))
    e.setFitnessOpr(FitnessKmPrecalculatedTSP(itemsDF, distancesDF))
    #e.setSelectionFnc(selectionTournamentFnc, [])
    e.setSelectionOpr(SelectionRoulette())
    e.setCrossoverOpr(CrossoverRtPMX())
    #e.setMutationFnc(mutationNothingFnc, [])
    #e.setMutationFnc(mutationSwapFnc, [])
    e.setMutationOpr(MutationRt2Opt())
    bestIndiv, bestFitness = e.run()

    lastPopulation:List
    lastPopFitness:List[float]
    lastPopulation, lastPopFitness = e.getPopAndFitnessValues(6)
    print(lastPopulation)
    print(lastPopFitness)

    indivDict = {}
    indivGPSDict = {}
    fitnessDict = {}
    for i in range(6):
        indivI = lastPopulation[i]
        indivGPSI = convertIndividualToGPS(indivI, itemsDF)
        fitnessI = lastPopFitness[i]

        indivDict[i] = indivI
        indivGPSDict[i] = indivGPSI
        fitnessDict[i] = fitnessI

    cherrypy.session['indivDict'] = indivDict
    cherrypy.session['indivGPSDict'] = indivGPSDict
    cherrypy.session['fitnessDict'] = fitnessDict

    shortLength = 15
    mediumLength = 30
    longLength = 50

    title0:str = "Short (" + str(shortLength) + " km) touristic roundtrip"
    title1:str = "Medium (" + str(mediumLength) + " km) touristic roundtrip"
    title2:str = "Long (" + str(longLength) + " km) touristic roundtrip"

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
            <h3 class="text-white display-1">Recommender TKY</h3>
            <div class="d-inline-flex text-white mb-5">
                <p class="m-0 text-uppercase"><a class="text-white" href="">Home</a></p>
                <i class="fa fa-angle-double-right pt-1 px-3"></i>
                <p class="m-0 text-uppercase">Recommender TKY</p>
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
   resultStr:str = """
    <div class="container-fluid py-5">
        <div class="container py-5">
            <div class="section-title text-center position-relative mb-4">
                <h1 class="display-4">""" + title + """</h1>
             </div>
            <div class="owl-carousel team-carousel position-relative" style="padding: 0 30px;">
            """
   mapCount = 6
   for colIDI in range(0,mapCount):
       fitnessStrI = str(cherrypy.session['fitnessDict'][colIDI])
       resultStr += """
                <div class="team-item">

                    <iframe width="400" height="400" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"
                        src="/mapOSM?row=""" + str(row) + """;column=""" + str(colIDI) + """" 
                        style="border: 1px solid black">
                    </iframe>

                    <br/><small><a href="/mapOSM?row=""" + str(row) + """;column=""" + str(colIDI) + """">View Larger Map</a></small>

                    <div class="bg-light text-center p-4">
                        <h5 class="mb-3">Indiv: """+str(colIDI)+"""</h5>
                        <p class="mb-2">Fitness: """+fitnessStrI+""" Km</p>
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
