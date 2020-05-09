#!/usr/bin/env python
# -*- encoding: utf8-*-

import requests
from bs4 import BeautifulSoup
import subprocess
import sys
import argparse
import json

def main( args ):

    parser = argparse.ArgumentParser("parse!");
    
    parser.add_argument( '-d', '--district', dest='district', default='Taipei', type=str )
    parser.add_argument( '-t', '--temperature', dest='temperature', default=False, type=bool )
    parser.add_argument( '-w', '--weather', dest='weather', default=False, type=bool )
    parser.add_argument( '-r', '--rain', dest='rain', default=False, type=bool )
    

    try:
        opt = parser.parse_args(args[1:])
    except:
        print "Error processing arguments!"
        parser.print_help()
        raise

    # help message for wrong district
    help_m = '''[WARNING] <District Error> 
There are some useful district choice :
{    
    Taipei  ,
    Hsinchu ,
    ...     ,
    ..      ,
    .
}
        '''

    reload(sys)
    sys.setdefaultencoding('utf-8')

    #url = "https://www.cwb.gov.tw/V8/C/W/OBS_Map.html"
    url = "https://www.cwb.gov.tw/Data/js/Observe/Observe_Home.js?"
    r = requests.get( url, allow_redirects=False )
    r.encoding = 'utf8'
    if r.status_code != 200 :
        return 
    soup = BeautifulSoup(r.text, 'html.parser')

    ts = (r.text).split('\n')

    ## tmp var
    l1 = ""
    
    for line in ts:
        if opt.district in line:
            l1 = str(line)
            break

    if l1 == "":
        print help_m
        return
    
    nl = json.loads( (l1.strip(' 0123456789:') + '}').replace('\'', '\"') )

    print     "District    : ", nl['CountyName']['C'], " ", nl['CountyName']['E']
    if (not opt.temperature) and (not opt.weather) and (not opt.rain) :
        print "Temperature : ", nl['Temperature']['C'], "C ", nl['Temperature']['F'], "F"
        print "Weather     : ", nl['Weather']['C'], " ", nl['Weather']['E']
        print "Rain Rate   : ", nl['Rain']['C'], " ", nl['Rain']['E']
    elif opt.temperature:
        print "Temperature : ", nl['Temperature']['C'], "C ", nl['Temperature']['F'], "F"
    elif opt.weather:
        print "Weather     : ", nl['Weather']['C'], " ", nl['Weather']['E']
    elif opt.rain:
        print "Rain Rate   : ", nl['Rain']['C'], " ", nl['Rain']['E']


    print "----- Data from 中央氣象局 -----"
    
    #print(r.history)
    #print(r.url)

    #for line in soup.find_all("span", class_="tem-C is-active"):
    #    print line
    #print soup.find_all("div", class_="tab-content")


if __name__ == '__main__':
   main( sys.argv )