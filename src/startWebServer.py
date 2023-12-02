#!/usr/bin/python3

import os
import cherrypy

from evaTour.webServer.index import Index


path   = os.path.abspath(os.path.dirname(__file__))
conf = {
  'global' : {
    'server.socket_host' : '127.0.0.1',
    'server.socket_port' : 8080,
    'server.thread_pool' : 8,
  },
  '/css' : {
    'tools.staticdir.on'    : True,
    'tools.staticdir.dir'   : os.path.join(path, 'evaTour/webServer/css'),
    'tools.gzip.on'         : True  
  },
  '/scss' : {
    'tools.staticdir.on'    : True,
    'tools.staticdir.dir'   : os.path.join(path, 'evaTour/webServer/scss'),
    'tools.gzip.on'         : True  
  },
  '/img' : {
    'tools.staticdir.on'    : True,
    'tools.staticdir.dir'   : os.path.join(path, 'evaTour/webServer/img'),
    'tools.gzip.on'         : True  
  },
  '/js' : {
    'tools.staticdir.on'    : True,
    'tools.staticdir.dir'   : os.path.join(path, 'evaTour/webServer/js'),
    'tools.gzip.on'         : True  
  },
  '/lib' : {
    'tools.staticdir.on'    : True,
    'tools.staticdir.dir'   : os.path.join(path, 'evaTour/webServer/lib'),
    'tools.gzip.on'         : True  
  },
  '/map' : {
    'tools.staticdir.on'    : True,
    'tools.staticdir.dir'   : os.path.join(path, 'evaTour/webServer/map'),
    'tools.gzip.on'         : True  
  }
}
cherrypy.config.update({'tools.sessions.on': True,
                        'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
                        'tools.sessions.storage_path': 'sessions',
                        'tools.sessions.timeout': 60
               })


def main():
    print("Starting web server!")
    os.chdir('../')

    cherrypy.quickstart(Index(), '/', conf)

if __name__ == "__main__":
    main()
