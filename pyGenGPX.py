#!/usr/bin/env python

# Based off cmdline boilerplate from:
# https://gist.github.com/opie4624/3896526
import sys, argparse, logging

# Import code to pull the data down
import urllib2, json, unicodedata, re

# Gather our code in a main() function
def main(args, loglevel):
  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
  
  logging.info( "Fetching data..." )
  logging.debug( "Fetching data from: %s" % args.url )

  req = urllib2.Request( args.url )

  response = urllib2.urlopen( req )

  # TODO Error handling...
  data = json.loads( response.read() )[ 'features' ]

  # Let's iterate through each trail
  logging.info( "Data received, parsing json" )
    
  for value in data:

      verbose_name = value[ 'properties' ][ 'NAME' ]
      filename = slugify( verbose_name ) + '.gpx'
      logging.info( "Creating GPX file for %s" % verbose_name )
      logging.debug( "Saving as: %s" % filename )

      f = open( filename, 'w+' )

      f.write( '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n' )
      f.write( '<gpx xmlns="http://www.topografix.com/GPX/1/1" creator="tmber" version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n' )
      f.write( '<trk>\n' )
      f.write( '<name>%s</name>\n' % verbose_name )
      f.write( '<trkseg>\n' )

      coords = value[ 'geometry' ][ 'coordinates' ]

      for latlon in coords:
           f.write( '<trkpt lat="%s" lon="%s"></trkpt>\n' % ( latlon[1], latlon[0] ) )

      f.write( '</trkseg>\n' )
      f.write( '</trk>\n' )
      f.write( '</gpx>\n' )


# Converts names into valid filenames      
def slugify ( value ):
    value = str( value )
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)
      
# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  parser = argparse.ArgumentParser( 
                                    description = "Does a thing to some stuff.",
                                    epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
                                    fromfile_prefix_chars = '@' )
  
  parser.add_argument(
                      "url",
                      help = "url to json object",
                      metavar = "url")
  # parser.add_argument(
  #                     "output",
  #                     help = "output file",
  #                     metavar = "output")
  parser.add_argument(
                      "-v",
                      "--verbose",
                      help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()
  
  # Setup logging
  if args.verbose:
    loglevel = logging.DEBUG
  else:
    loglevel = logging.INFO
  
  main(args, loglevel)
