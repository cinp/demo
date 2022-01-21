#!/usr/bin/env python3

import os

os.environ.setdefault( 'DJANGO_SETTINGS_MODULE', 'demo.settings' )

import django
django.setup()

import sys
import logging

from gunicorn.app.base import BaseApplication

from cinp.server_werkzeug import WerkzeugServer

from demo.Auth.models import getUser

DEBUG = True


class GunicornApp( BaseApplication ):
  def __init__( self, application, options=None ):
    self.options = options or {}
    self.application = application
    super().__init__()

  def load_config( self ):
    for ( key, value ) in self.options.items():
      self.cfg.set( key.lower(), value )

  def load( self ):
    return self.application


if __name__ == '__main__':
  logging.basicConfig()
  logger = logging.getLogger()
  logger.setLevel( logging.DEBUG )
  logger.info( 'Starting up...' )

  logger.debug( 'Creating Server...' )
  app = WerkzeugServer( root_path='/api/v1/', root_version='1.0', debug=DEBUG, get_user=getUser, cors_allow_list=[ '*' ], debug_dump_location=None )
  logger.debug( 'Registering Models...' )

  app.registerNamespace( '/', 'demo.Auth' )
  app.registerNamespace( '/', 'demo.Car' )

  logger.info( 'Validating...' )
  app.validate()

  logger.info( 'Starting Server...' )
  GunicornApp( app, { 'bind': '0.0.0.0:8888', 'loglevel': 'debug' } ).run()
  logger.info( 'Server Done...' )
  logger.info( 'Shutting Down...' )
  logger.info( 'Done!' )
  logger.shutdown
  sys.exit( 0 )
