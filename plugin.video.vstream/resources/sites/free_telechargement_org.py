#-*- coding: utf-8 -*-

from resources.lib.config import cConfig
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.favourite import cFav
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.cloudflare import CloudflareBypass
from resources.lib.cloudflare import NoRedirection


import urllib,re,urllib2
import xbmcgui
import xbmc
import xbmcaddon,os

PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile"))
UA = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

SITE_IDENTIFIER = 'free_telechargement_org' 
SITE_NAME = '[COLOR violet]Free-telechargement[/COLOR]' 
SITE_DESC = 'Fichier en DDL, HD' 

URL_MAIN = 'http://www.free-telechargement.org/'
URL_PROTECT = 'http://liens.free-telechargement.org/'

URL_SEARCH_MOVIES_SD = (URL_MAIN + '1/recherche1/1.html?rech_cat=video&rech_fiche=', 'showMovies')
URL_SEARCH_MOVIES_HD = (URL_MAIN + '1/recherche1/1.html?rech_cat=Films+HD&rech_fiche=', 'showMovies')

URL_SEARCH_SERIES_SD = (URL_MAIN + '1/recherche1/1.html?rech_cat=serie&rech_fiche=', 'showMovies')
URL_SEARCH_SERIES_HD = (URL_MAIN + '1/recherche1/1.html?rech_cat=seriehd&rech_fiche=', 'showMovies')


URL_SEARCH_ANIMES = (URL_MAIN, 'showMovies')
URL_SEARCH_MANGAS = (URL_MAIN, 'showMovies')
URL_SEARCH_EMISSIONS_TV = (URL_MAIN, 'showMovies')
URL_SEARCH_SPECTACLES = (URL_MAIN, 'showMovies')


URL_SEARCH = (URL_MAIN + '1/recherche1/1.html?rech_fiche=', 'showMovies')

FUNCTION_SEARCH = 'showMovies'

MOVIE_SD_DVDRIP = (URL_MAIN + '1/categorie-Films+DVDRiP+et+BDRiP/1.html', 'showMovies') # derniers films en SD
MOVIE_SD_CAM = (URL_MAIN + '1/categorie-Films+CAM+TS+R5+et+DVDSCR/1.html', 'showMovies') # derniers films en SD
MOVIE_SD_VOSTFR = (URL_MAIN + '1/categorie-Films+VOSTFR+et+VO/1.html', 'showMovies') # derniers films en SD
MOVIE_SD_CLASSIQUE = (URL_MAIN + '1/categorie-Films+Classiques/1.html', 'showMovies') # derniers films en SD
MOVIE_SD_VIEWS = (URL_MAIN + '1/films/affichage', 'showMovies') # derniers films en SD
MOVIE_GENRES_SD = (True, 'showGenreMoviesSD')

MOVIE_HD = (URL_MAIN + '1/categorie-Films+BluRay+720p+et+1080p/1.html', 'showMovies') # derniers films en HD
MOVIE_3D = (URL_MAIN + '1/categorie-Films+BluRay+3D/1.html', 'showMovies') # derniers films en 3D
MOVIE_HD_VIEWS = (URL_MAIN + '1/films-bluray/affichage', 'showMovies') # derniers films en HD
MOVIE_GENRES_HD = (True, 'showGenreMoviesHD')

ANIMES = (URL_MAIN + '1/animations/1', 'showMovies') # derniers dessins animés

MANGAS_VF = (URL_MAIN + '1/categorie-Mangas+VF/1.html', 'showMovies') # derniers dessins animés
MANGAS_VOST = (URL_MAIN + '1/categorie-Mangas+VOST/1.html', 'showMovies') # derniers dessins animés

EMISSIONS_TV = (URL_MAIN + '1/categorie-Emissions/1.html', 'showMovies') # dernieres émissions TV

SPECTACLES = (URL_MAIN + '1/categorie-Spectacles/1.html', 'showMovies') # dernieres émissions TV

SERIES_SD_EN_COURS_VF = (URL_MAIN + '1/categorie-Saisons+en+cours+VF+/', 'showMovies') # derniers films en SD
SERIES_SD_EN_COURS_VOSTFR = (URL_MAIN + '1/categorie-Saisons+en+cours+VOST/', 'showMovies') # derniers films en SD
SERIES_SD_TERMINE_VF = (URL_MAIN + '1/categorie-Saison+Terminée+VF/', 'showMovies') # derniers films en SD
SERIES_SD_TERMINE_VOSTFR = (URL_MAIN + '1/categorie-Saison+Terminée+VOST/', 'showMovies') # derniers films en SD
SERIES_HD_EN_COURS_VF = (URL_MAIN + '1/categorie-Saisons+en+cours+VF+HD/', 'showMovies') # derniers films en SD
SERIES_HD_EN_COURS_VOSTFR = (URL_MAIN + '1/categorie-Saisons+en+cours+VOST+HD/', 'showMovies') # derniers films en SD
SERIES_HD_TERMINE_VF = (URL_MAIN + '1/categorie-Saison+Terminée+VF+HD/', 'showMovies') # derniers films en SD
SERIES_HD_TERMINE_VOSTFR = (URL_MAIN + '1/categorie-Saison+Terminée+VOST+HD/', 'showMovies') # derniers films en SD

def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler)  
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    #oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Series', 'series.png', oOutputParameterHandler)      

    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    #oGui.addDir(SITE_IDENTIFIER, 'showMenuDessinsAnimes', 'Dessins Animés', 'animes.png', oOutputParameterHandler)    
   
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    #oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Mangas', 'animes.png', oOutputParameterHandler)    
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSpectacles', 'Spectacles', 'films.png', oOutputParameterHandler)    
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuEmissionsTV', 'Emissions TV', 'tv.png', oOutputParameterHandler)    
    
    oGui.setEndOfDirectory() 

def showMenuFilms():
    oGui = cGui()
       
    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMoviesSD', 'Recherche de films SD', 'search.png', oOutputParameterHandler) 

    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMoviesHD', 'Recherche de films HD', 'search.png', oOutputParameterHandler) 

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_VIEWS[1], 'Films SD les plus vus', 'films.png', oOutputParameterHandler)  
     
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_DVDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_DVDRIP[1], 'Derniers Films SD DVDRIP et BDRIP ajoutes', 'news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_CAM[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_CAM[1], 'Derniers Films SD CAM et DVDScr ajoutes', 'news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_VOSTFR[1], 'Derniers Films SD VOSTFR ajoutes', 'news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_CLASSIQUE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_CLASSIQUE[1], 'Derniers Films SD Classiques ajoutes', 'news.png', oOutputParameterHandler)  
     
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Derniers Films HD 720p et 1080p ajoutes', 'news.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Derniers Films en 3D ajoutes', 'news.png', oOutputParameterHandler) 
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD_VIEWS[1], 'Films HD les plus vus', 'films.png', oOutputParameterHandler)  
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES_SD[0])
    #oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES_SD[1], 'Films SD par Genre', 'genres.png', oOutputParameterHandler)

    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES_HD[0])
    #oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES_HD[1], 'Films HD par Genre', 'genres.png', oOutputParameterHandler)
     
    oGui.setEndOfDirectory()     

def showMenuSeries():
    oGui = cGui()
       
    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Recherche de series', 'search.png', oOutputParameterHandler)
        
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_SD_EN_COURS_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_SD_EN_COURS_VF[1], 'Séries SD VF en cours', 'news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_SD_EN_COURS_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_SD_EN_COURS_VOSTFR[1], 'Séries SD VOSTFR en cours', 'news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_SD_TERMINE_VF_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_SD_TERMINE_VF[1], 'Séries SD VF terminées', 'news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_SD_TERMINE_VOSTFR_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_SD_TERMINE_VOSTFR[1], 'Séries SD VOSTFR terminées', 'news.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_HD_EN_COURS_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_HD_EN_COURS_VF[1], 'Séries HD VF en cours', 'news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_HD_EN_COURS_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_HD_EN_COURS_VOSTFR[1], 'Séries HD VOSTFR en cours', 'news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_HD_TERMINE_VF_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_HD_TERMINE_VF[1], 'Séries HD VF terminées', 'news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_HD_TERMINE_VOSTFR_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_HD_TERMINE_VOSTFR[1], 'Séries HD VOSTFR terminées', 'news.png', oOutputParameterHandler)  
     
    
    oGui.setEndOfDirectory()     
    
def showMenuDessinsAnimes():
    oGui = cGui()
       
    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearchAnimes', 'Recherche de Dessins Animés', 'search.png', oOutputParameterHandler) 
        
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIMES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIMES[1], 'Derniers Dessins Animés ajoutés', 'news.png', oOutputParameterHandler)  
    
    oGui.setEndOfDirectory()     

def showMenuMangas():
    oGui = cGui()
       
    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMangas', 'Recherche de Mangas', 'search.png', oOutputParameterHandler) 
        
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MANGAS_VF[0])
    oGui.addDir(SITE_IDENTIFIER, MANGAS_VF[1], 'Derniers Mangas VF ajoutés', 'news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MANGAS_VOST[0])
    oGui.addDir(SITE_IDENTIFIER, MANGAS_VOST[1], 'Derniers Mangas VOSTFR ajoutés', 'news.png', oOutputParameterHandler)  
        
    oGui.setEndOfDirectory()     

def showMenuSpectacles():
    oGui = cGui()
       
    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSpectacles', 'Recherche de Spectacles', 'search.png', oOutputParameterHandler) 
        
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPECTACLES[0])
    oGui.addDir(SITE_IDENTIFIER, SPECTACLES[1], 'Derniers Spectacles ajoutés', 'news.png', oOutputParameterHandler)  
    
    oGui.setEndOfDirectory()         
    
def showMenuEmissionsTV():
    oGui = cGui()
       
    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearchEmissionsTV', 'Recherche d Emissions TV', 'search.png', oOutputParameterHandler) 
        
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', EMISSIONS_TV[0])
    oGui.addDir(SITE_IDENTIFIER, EMISSIONS_TV[1], 'Dernieres Emissions TV', 'news.png', oOutputParameterHandler)  
    
    oGui.setEndOfDirectory()     
           
def showSearchMovies(): 
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH_MOVIES[0] + sSearchText
        showMovies(sUrl) 
        oGui.setEndOfDirectory()
        return
    
def showSearchSeries(): 
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH_SERIES[0] + sSearchText
        showMovies(sUrl) 
        oGui.setEndOfDirectory()
        return

def showSearchAnimes(): 
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH_ANIMES[0] + sSearchText
        showMovies(sUrl) 
        oGui.setEndOfDirectory()
        return        
 
def showSearchMangas(): 
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH_MANGAS[0] + sSearchText
        showMovies(sUrl) 
        oGui.setEndOfDirectory()
        return    

def showSearchSpectacles(): 
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH_SPECTACLES[0] + sSearchText
        showMovies(sUrl) 
        oGui.setEndOfDirectory()
        return    
               
def showSearchEmissionsTV(): 
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH_EMISSIONS_TV[0] + sSearchText
        showMovies(sUrl) 
        oGui.setEndOfDirectory()
        return    
      
def showGenreMoviesSD(): 
    showGenre("films-1.html&order=2")
 
def showGenreMoviesHD(): 
    showGenre("films-hd-13.html&order=2")

def showGenreSeriesSD(): 
    showGenre("series-tv-6.html")

def showGenreSeriesHD(): 
    showGenre("series-hd-20.html")

def showGenre(basePath): 
    oGui = cGui()
    
    liste = []
    liste.append( ['Action',URL_MAIN + 'telechargement+5/' + basePath] )
    liste.append( ['Animation',URL_MAIN + 'telechargement+4/' + basePath] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'telechargement+64/' + basePath] )
    liste.append( ['Aventure',URL_MAIN + 'telechargement+20/' + basePath] )
    liste.append( ['Biographie',URL_MAIN + 'telechargement+38/' + basePath] )
    liste.append( ['Biopic',URL_MAIN + 'telechargement+28/' + basePath] )
    liste.append( ['Combat',URL_MAIN + 'telechargement+35/' + basePath] )
    liste.append( ['Comédie',URL_MAIN + 'telechargement+1/' + basePath] )
    liste.append( ['Comédie dramatique',URL_MAIN + 'telechargement+12/' + basePath] )
    liste.append( ['Comédie musicale',URL_MAIN + 'telechargement+33/' + basePath] )
    liste.append( ['Comédie romantique',URL_MAIN + 'telechargement+53/' + basePath] )
    liste.append( ['Comique',URL_MAIN + 'telechargement+51/' + basePath] )
    liste.append( ['Court métrage',URL_MAIN + 'telechargement+45/' + basePath] )
    liste.append( ['Criminalité',URL_MAIN + 'telechargement+40/' + basePath] )
    liste.append( ['Dessin animé',URL_MAIN + 'telechargement+27/' + basePath] )
    liste.append( ['Divers',URL_MAIN + 'telechargement+34/' + basePath] )
    liste.append( ['Divertissement',URL_MAIN + 'telechargement+66/' + basePath] )
    liste.append( ['Documentaire',URL_MAIN + 'telechargement+9/' + basePath] )
    liste.append( ['Drame',URL_MAIN + 'telechargement+3/' + basePath] )
    liste.append( ['Epouvante',URL_MAIN + 'telechargement+41/' + basePath] )
    liste.append( ['Epouvante-horreur',URL_MAIN + 'telechargement+17/' + basePath] )
    liste.append( ['Erotique',URL_MAIN + 'telechargement+24/' + basePath] ) 
    liste.append( ['Espionnage',URL_MAIN + 'telechargement+13/' + basePath] ) 
    liste.append( ['Famille',URL_MAIN + 'telechargement+31/' + basePath] ) 
    liste.append( ['Fantastique',URL_MAIN + 'telechargement+16/' + basePath] ) 
    liste.append( ['Guerre',URL_MAIN + 'telechargement+22/' + basePath] ) 
    liste.append( ['Historique',URL_MAIN + 'telechargement+21/' + basePath] ) 
    liste.append( ['Horreur',URL_MAIN + 'telechargement+15/' + basePath] ) 
    liste.append( ['Humour',URL_MAIN + 'telechargement+44/' + basePath] ) 
    liste.append( ['Jeunesse',URL_MAIN + 'telechargement+19/' + basePath] ) 
    liste.append( ['Judiciaire',URL_MAIN + 'telechargement+67/' + basePath] ) 
    liste.append( ['Manga',URL_MAIN + 'telechargement+58/' + basePath] ) 
    liste.append( ['Médical',URL_MAIN + 'telechargement+47/' + basePath] ) 
    liste.append( ['Musical',URL_MAIN + 'telechargement+10/' + basePath] ) 
    liste.append( ['Mystère',URL_MAIN + 'telechargement+26/' + basePath] ) 
    liste.append( ['Péplum',URL_MAIN + 'telechargement+54/' + basePath] ) 
    liste.append( ['Policier',URL_MAIN + 'telechargement+2/' + basePath] ) 
    liste.append( ['Romance',URL_MAIN + 'telechargement+6/' + basePath] ) 
    liste.append( ['Science fiction',URL_MAIN + 'telechargement+7/' + basePath] ) 
    liste.append( ['Spectacle',URL_MAIN + 'telechargement+39/' + basePath] ) 
    liste.append( ['Sport',URL_MAIN + 'telechargement+68/' + basePath] ) 
    liste.append( ['Thriller',URL_MAIN + 'telechargement+8/' + basePath] ) 
    liste.append( ['Western',URL_MAIN + 'telechargement+11/' + basePath] ) 
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)    
       
    oGui.setEndOfDirectory() 
        
def showMovies(sSearch = ''):
    oGui = cGui()
    bGlobal_Search = False
    if sSearch:
        
        #par defaut
        sUrl = sSearch
        
        if URL_SEARCH[0] in sSearch:
            bGlobal_Search = True
        
        #partie en test
        oInputParameterHandler = cInputParameterHandler()
        sType = oInputParameterHandler.getValue('type') 
      
        if sType:
            if sType == "film":
                sUrl = sUrl.replace(URL_SEARCH[0], URL_SEARCH_MOVIES[0])
            if sType == "serie":
                sUrl = sUrl.replace(URL_SEARCH[0], URL_SEARCH_SERIES[0])
            if sType == "anime":
                sUrl = sUrl.replace(URL_SEARCH[0], URL_SEARCH_ANIMS[0])

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') 
        
    #xbmc.log(sUrl)
    oRequestHandler = cRequestHandler(sUrl) 
    sHtmlContent = oRequestHandler.request()
    #xbmc.log(sHtmlContent)
    sCom = ''
    sQual = ''
    sPattern = '<table style="float:left;padding-left:8px"> *<td> *<div align="left"> *<a href="([^"]+)" onmouseover="Tip\(\'<b>([^"]+?)<\/b>.+?Description :</b> <i>([^<]+?)<.+?<img src="([^"]+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    xbmc.log(str(aResult))
    
    if (aResult[0] == True):
        total = len(aResult[1])        
        for aEntry in aResult[1]:
            sQual = 'SD'
            if '-hd/' in aEntry[0] or 'bluray' in aEntry[0]:
                sQual = 'HD'
            if '-3d/' in aEntry[0]:
                sQual = '3D'
            sCom = str(aEntry[2])
            sTitle = str(aEntry[1])
            sUrl2 = aEntry[0]
            #xbmc.log(sUrl2)
            #sFanart =aEntry[1]
            sThumbnail=aEntry[3]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(sUrl2)) 
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle)) 
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sCom', sCom)
            sDisplayTitle = cUtil().DecoTitle('('+sQual+') '+sTitle)
            
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumbnail, sCom, oOutputParameterHandler)
            

        sNextPage = __checkForNextPage(sHtmlContent)#cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    #tPassage en mode vignette sauf en cas de recherche globale
    if not bGlobal_Search:
        xbmc.executebuiltin('Container.SetViewMode(500)')
    
     
    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class="desactive">« préc</span>  <span class="courante">[^<]+</span> <a href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        xbmc.log(str(aResult))
        return URL_MAIN+aResult[1][0]
        
    return False

def showLinks():
    xbmc.log('showLinks')
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if 'series' in sUrl:
        showHosters()
    else:
        showHosters()
    
    return


def showHosters():# recherche et affiche les hotes
    xbmc.log("showHosters")
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler() 
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')
    
    xbmc.log(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #xbmc.log(sHtmlContent)
    oParser = cParser()
    
    #recuperation nom de la release
    if 'elease :' in sHtmlContent:
        sPattern = 'elease :([^<]+)<'
    else:
        sPattern = '<br /> *([^<]+)</p></center>'
    
    aResult1 = oParser.parse(sHtmlContent, sPattern)
    if (aResult1[0] == True):
        if 'Forced' in aResult1[1][0]: aResult1[1][0]=''
    xbmc.log(str(aResult1))
    
    #cut de la zone des liens
    if 'Lien Premium  --' in sHtmlContent:
        sPattern = 'Lien Premium  --(.+?)</div>'
    else:
        sPattern = '<div id="link">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sHtmlContent = aResult[1][0]
    sHtmlContent = re.sub('<font color="[^"]+">','',sHtmlContent)
    sHtmlContent = re.sub('</font>','',sHtmlContent)
    #sHtmlContent = re.sub('link.php\?lien\=','',sHtmlContent)
             
    xbmc.log(sHtmlContent)
    
    if '-multi' in sHtmlContent:
        sPattern = '<a href="link.php\?lien\=([^"]+)"'
    else:
        sPattern = '<b>(.+?)</b> </br> <a href="link.php\?lien\=([^"]+)" target="_blank" ><b>Cliquer ici pour Télécharger</b></a><br /><br />'
   
    aResult = oParser.parse(sHtmlContent, sPattern)
    xbmc.log(str(aResult))
       
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        oGui.addText(SITE_IDENTIFIER, aResult1[1][0])
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            oOutputParameterHandler = cOutputParameterHandler()
            if total == 1:
                sTitle = '[COLOR skyblue]' + 'Liens Premium' + '[/COLOR] '
                oOutputParameterHandler.addParameter('siteUrl', aEntry)
            else:
                sTitle = '[COLOR skyblue]' + aEntry[0]+ '[/COLOR] '
                oOutputParameterHandler.addParameter('siteUrl', aEntry[1])
            
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumbnail, '', oOutputParameterHandler)
   
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
  
def Display_protected_link():
    xbmc.log("Display_protected_link")
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')

    oParser = cParser()
    xbmc.log(sUrl)
    
    #Est ce un lien dl-protect ?
    if URL_PROTECT in sUrl:
        sHtmlContent = DecryptddlProtect(sUrl) 
        #xbmc.log(sHtmlContent)
        if sHtmlContent:
            #Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotect = (True, [sHtmlContent])
            else:
                sPattern_dlprotect = 'target=_blank>([^<]+)<'
                aResult_dlprotect = oParser.parse(sHtmlContent, sPattern_dlprotect)
                
        else:
            oDialog = cConfig().createDialogOK('Desole, probleme de captcha.\n Veuillez en rentrer un directement sur le site, le temps de reparer')
            aResult_dlprotect = (False, False)

    #Si lien normal       
    else:
        if not sUrl.startswith('http'):
            sUrl = 'http://' + sUrl
        aResult_dlprotect = (True, [sUrl]) 
        
    #xbmc.log(aResult_dlprotect)
        
    if (aResult_dlprotect[0]):
            
        
        
        for aEntry in aResult_dlprotect[1]:
            sHosterUrl = aEntry
            #xbmc.log(sHosterUrl)
            
            sTitle = sMovieTitle
            
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
                        
    oGui.setEndOfDirectory()

def DecryptddlProtect(url):
    xbmc.log("DecryptddlProtect")
    
    xbmc.log('>>' + url)
    
    if not (url): return ''
    
    cookies = ''
    #try to get previous cookie
    cookies = Readcookie('liens_free-telechargement_org')
    xbmc.log( 'cookie récupéré:')
    xbmc.log( 'Ancien' + cookies )
    oRequestHandler = cRequestHandler(url)
    if cookies:
        oRequestHandler.addHeaderEntry('Cookie',cookies)
    sHtmlContent = oRequestHandler.request()
    
    #A partir de la on a les bon cookies pr la protection cloudflare

    #Si ca demande le captcha
    if 'Veuillez recopier le captcha ci-dessus' in sHtmlContent:

        s = re.findall('src=".\/([^<>"]+?)" alt="CAPTCHA Image"',sHtmlContent)
        if URL_PROTECT in s[0]:
            image = s[0]
        else:
            image = URL_PROTECT + s[0]
            
        xbmc.log(image)

        captcha,cookies2 = get_response(image,cookies)
        cookies = cookies + '; ' +cookies2
        xbmc.log( 'New ' + cookies)
        
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent' , UA)
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4')
        oRequestHandler.addHeaderEntry('Accept' , 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('Cookie',cookies)
        oRequestHandler.addHeaderEntry('Referer',url)
        
        oRequestHandler.addParameters( 'do' , 'contact')
        oRequestHandler.addParameters( 'ct_captcha' , captcha)
        
        sHtmlContent = oRequestHandler.request()
        
        #xbmc.log( sHtmlContent )
        
        if 'Code de securite incorrect' in sHtmlContent:
            cGui().showInfo("Erreur", 'Mauvais Captcha' , 5)
            return 'rate'
        
        if 'Veuillez recopier le captcha ci-dessus' in sHtmlContent:
            cGui().showInfo("Erreur", 'Rattage' , 5)
            return 'rate'
            
        #si captcha reussi
        #save cookies
        SaveCookie('liens_free-telechargement_org',cookies)        
    
    return sHtmlContent  

def DeleteCookie(Domain):
    file = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')
    os.remove(os.path.join(PathCache,file))
    
def SaveCookie(Domain,data):
    Name = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')

    #save it
    file = open(Name,'w')
    file.write(data)

    file.close()
    
def Readcookie(Domain):
    Name = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')
    
    try:
        file = open(Name,'r')
        data = file.read()
        file.close()
    except:
        return ''
    
    return data
	
def get_response(img,cookie):    
    xbmc.log( "get_reponse")
    #on telecharge l'image
    filename  = os.path.join(PathCache,'Captcha.png')

    hostComplet = re.sub(r'(https*:\/\/[^/]+)(\/*.*)','\\1',img)
    host = re.sub(r'https*:\/\/','',hostComplet)
    url = img                 


    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent' , UA)
    #oRequestHandler.addHeaderEntry('Referer', url)
    oRequestHandler.addHeaderEntry('Cookie',cookie)
      
    htmlcontent = oRequestHandler.request()
    
    NewCookie = oRequestHandler.GetCookies()

    
    downloaded_image = file(filename, "wb")
    downloaded_image.write(htmlcontent)
    downloaded_image.close()
           
    #on affiche le dialogue
    solution = ''
    try:
        img = xbmcgui.ControlImage(450, 0, 400, 130, filename)
        wdlg = xbmcgui.WindowDialog()
        wdlg.addControl(img)
        wdlg.show()
        #xbmc.sleep(3000)
        kb = xbmc.Keyboard('', 'Tapez les Lettres/chiffres de l\'image', False)
        kb.doModal()
        if (kb.isConfirmed()):
            solution = kb.getText()
            if solution == '':
                cGui().showInfo("Erreur", 'Vous devez taper le captcha' , 4)
        else:
            cGui().showInfo("Erreur", 'Vous devez taper le captcha' , 4)
    finally:
        wdlg.removeControl(img)
        wdlg.close()
        
    return solution,NewCookie