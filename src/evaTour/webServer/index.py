#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from evaTour.datasets.usersSimilarity import readSimilarityDFNYC, readSimilarityDFTKY
from evaTour.maps.openStreetMaps import convertIndividualToGPS
from evaTour.recommenders.recommenderSVDS import RecommenderSVDS
from evaTour.webServer.GroupRecommendationNYCPage import getGroupRecommenderPage
from evaTour.webServer.MapOSMPointsPage import getMapOSMVisitedPointsPage, getMapOSMRecommendedPointsPage
from evaTour.webServer.TeamsPage import getTeamsPage
from evaTour.webServer.UserDetailPage import getUserDetailPage
from evaTour.webServer.datamodels.UsersModel import UsersModel
from evaTour.webServer.datamodels.TeamsModel import TeamsModel

from evaTour.webServer.HomePage import getHomePage
from evaTour.webServer.LogInPage import getLogInPage
from evaTour.webServer.ContributionPage import getContributionPage
from evaTour.webServer.DataPage import getDataPage
from evaTour.webServer._DetailPage import getDetailPage
from evaTour.webServer._FeaturePage import getFeaturePage
from evaTour.webServer.RecommenderNYCPage import getRecommenderNYCPage
from evaTour.webServer.RecommenderNYC2Page import getRecommenderNYC2Page
from evaTour.webServer.RecommenderTKYPage import getRecommenderTKYPage
from evaTour.webServer.RecommenderTKY2Page import getRecommenderTKY2Page
from evaTour.webServer.TestimonialPage import getTestimonialPage
from evaTour.webServer.ContactPage import getContactPage
from evaTour.webServer.MapOSMRoundtripPage import getMapOSMRoundtripPage

from evaTour.datasets.datasetFoursquare import readDatasetNYC
from evaTour.datasets.datasetFoursquare import readDatasetTKY

from evaTour.datasets.datasetFoursquare import getVisitedPlacesOfUser

from pandas import DataFrame
from pandas import Series
from typing import List

import cherrypy


class Index(object):
    ratingsNYcDF:DataFrame
    itemsNYcDF:DataFrame
    distancesNYcDF:DataFrame
    ratingsTkyDF:DataFrame
    itemsTkyDF:DataFrame
    distancesTkyDF:DataFrame

    usersModel:UsersModel

    def __init__(self):
        self.ratingsNYcDF, self.itemsNYcDF, self.distancesNYcDF = readDatasetNYC()
        self.ratingsTkyDF, self.itemsTkyDF, self.distancesTkyDF = readDatasetTKY()
        self.similarityDFNYC = readSimilarityDFNYC()
        self.similarityDFTKY = readSimilarityDFTKY()

        self.rNYcSVDS = RecommenderSVDS({RecommenderSVDS.ARG_K: 8})
        self.rNYcSVDS.train(self.ratingsNYcDF, self.itemsNYcDF, self.distancesNYcDF)

        self.rTkySVDS = RecommenderSVDS({RecommenderSVDS.ARG_K: 8})
        self.rTkySVDS.train(self.ratingsTkyDF, self.itemsTkyDF.copy(), self.distancesTkyDF)

        self.usersModel = UsersModel.readModel()
        self.teamsModel = TeamsModel.readModel()

    @cherrypy.expose
    def home(self):
        return getHomePage()
    
    index_shtml = index_html = index_htm = index_php = index = home

    @cherrypy.expose
    def log_in(self, userName:str=""):
        return getLogInPage(userName)

    @cherrypy.expose
    def log_in_finished(self, userName:str, passwd:str):
        if not self.usersModel.authorize(userName, passwd):
            return getLogInPage(userName, True)

        userID = self.usersModel.getUserIDFromUserName(userName)
        cherrypy.session['username'] = userName
        cherrypy.session['userid'] = userID

        isLogined:bool = cherrypy.session.get('username') != None

        raise cherrypy.HTTPRedirect('/home')

    @cherrypy.expose
    def log_out(self):
        cherrypy.session['username'] = None
        raise cherrypy.HTTPRedirect('/home')


    @cherrypy.expose
    def contribution(self):
        return getContributionPage()

    @cherrypy.expose
    def data(self):
        return getDataPage()


#    @cherrypy.expose
#    def detail(self):
#        return getDetailPage()
#
#    @cherrypy.expose
#    def feature(self):
#        return getFeaturePage()


    @cherrypy.expose
    def recommender_nyc(self):
        userID = cherrypy.session.get('userid')
        userName = cherrypy.session.get('username')
        if userID == None:
            return getLogInPage(userName)
        return getRecommenderNYCPage(self.ratingsNYcDF, self.itemsNYcDF, self.distancesNYcDF)

    @cherrypy.expose
    def recommender_nyc2(self):
        userID = cherrypy.session.get('userid')
        userName = cherrypy.session.get('username')
        return getRecommenderNYC2Page(userID, self.rNYcSVDS, self.ratingsNYcDF, self.itemsNYcDF, self.distancesNYcDF)

    @cherrypy.expose
    def recommender_tky(self):
        return getRecommenderTKYPage(self.ratingsTkyDF, self.itemsTkyDF, self.distancesTkyDF)

    @cherrypy.expose
    def recommender_tky2(self):
        return getRecommenderTKY2Page()


    @cherrypy.expose
    def group_recommender(self, teamID):
        userID = cherrypy.session.get('userid')
        destination = self.teamsModel.getTeamDestination(teamID)
        print("destination: " + str(destination))
        if destination == TeamsModel.DESTINATION_NYC:
            return getGroupRecommenderPage(userID, teamID, self.usersModel, self.teamsModel,
                        self.rNYcSVDS, self.ratingsNYcDF, self.itemsNYcDF, self.distancesNYcDF)
        elif destination == TeamsModel.DESTINATION_TKY:
            return getGroupRecommenderPage(userID, teamID, self.usersModel, self.teamsModel,
                        self.rTkySVDS, self.ratingsTkyDF, self.itemsTkyDF, self.distancesTkyDF)
        else:
            print("chyba")

    @cherrypy.expose
    def testimonial(self):
        return getTestimonialPage()

    @cherrypy.expose
    def teams(self, selTeamID=None):
        userID = int(cherrypy.session.get('userid'))

        if userID == None:
            raise cherrypy.HTTPRedirect('/log_in')

        teamsIDsOfUser = self.teamsModel.getTeamIDsWhereUserIDBelongs(int(userID))
        #print("teamsIDsOfUser: " + str(teamsIDsOfUser))

        teamsOfUser = self.teamsModel.exportTeamModelOfTeamIDs(teamsIDsOfUser)
        destination = teamsOfUser.getTeamDestination(selTeamID)

        usersModelOfDestination = self.usersModel.exportUserModelOfDestionation(destination)

        return getTeamsPage(userID, teamsOfUser, usersModelOfDestination, self.similarityDFNYC, self.similarityDFTKY, selTeamID)

    @cherrypy.expose
    def team_add(self, teamName, destination, userID):
        #print("teamName: " + str(teamName))
        #print("destination: " + str(destination))
        #print("userID to add: " + str(userID))
        teamID = self.teamsModel.addTeam(teamName, destination)
        self.teamsModel.addUserToTeam(userID, teamID)
        self.teamsModel.saveModel()

        raise cherrypy.HTTPRedirect('/teams')

    @cherrypy.expose
    def team_delete(self, teamID):
        #print("teamID: " + str(teamID))
        self.teamsModel.removeTeam(int(teamID))
        self.teamsModel.saveModel()

        raise cherrypy.HTTPRedirect('/teams')

    @cherrypy.expose
    def team_add_new_user(self, userID, teamID):
        #print("userID to add: " + str(userID))
        #print("teamID to add: " + str(teamID))

        self.teamsModel.addUserToTeam(int(userID), int(teamID))
        self.teamsModel.saveModel()

        raise cherrypy.HTTPRedirect('/teams')

    @cherrypy.expose
    def team_del_user(self, userID, teamID):
        #print("userID to del: " + str(userID))
        #print("teamID to del: " + str(teamID))

        self.teamsModel.removeUserFromTeam(int(userID), int(teamID))
        self.teamsModel.saveModel()

        raise cherrypy.HTTPRedirect('/teams')

    @cherrypy.expose
    def user_detail(self, userID):
        userName:str = self.usersModel.getUsername(int(userID))

        changedUserID = userID
        if str(userName).startswith("nyc"):
            changedUserID:int = self.usersModel.getNYCUserIDFromUserID(int(userID))
            visitedVenueIDs, visitedVenueCategoryNames, visitedGPSCoords = getVisitedPlacesOfUser(
                        changedUserID, self.ratingsNYcDF, self.itemsNYcDF)
        if str(userName).startswith("tky"):
            changedUserID:int = self.usersModel.getTKYUserIDFromUserID(int(userID))
            visitedVenueIDs, visitedVenueCategoryNames, visitedGPSCoords = getVisitedPlacesOfUser(
                        changedUserID, self.ratingsTkyDF, self.itemsTkyDF)

        if str(userName).startswith("nyc"):
            recommendation:Series = self.rNYcSVDS.recommend(changedUserID, 100)
            recItemIDs:List = list(recommendation.keys())
            #scores:List = list(recommendation.values)
            recGPSCoords = convertIndividualToGPS(recItemIDs, self.itemsNYcDF)

        if str(userName).startswith("tky"):
            recommendation:Series = self.rTkySVDS.recommend(changedUserID, 100)
            recItemIDs:List = list(recommendation.keys())
            #scores:List = list(recommendation.values)
            recGPSCoords = convertIndividualToGPS(recItemIDs, self.itemsTkyDF)

        #print("visitedVenueIDs: " + str(visitedVenueIDs))
        #print("recItemIDs: " + str(recItemIDs))

        return getUserDetailPage(changedUserID, userName, visitedVenueIDs, visitedVenueCategoryNames, visitedGPSCoords,
                                 recItemIDs, None, recGPSCoords)

    @cherrypy.expose
    def contact(self):
        return getContactPage()

    @cherrypy.expose
    def mapOSM(self, row=0, column=0):
        return getMapOSMRoundtripPage(row, column)

    @cherrypy.expose
    def map_osm_visited_points(self, userID):
        return getMapOSMVisitedPointsPage(userID)

    @cherrypy.expose
    def map_osm_recommended_points(self, userID):
        return getMapOSMRecommendedPointsPage(userID)