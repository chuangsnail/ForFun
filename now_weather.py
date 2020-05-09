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
    parser.add_argument( '-u', '--humidity', dest='humidity', default=False, type=bool )
    

    try:
        opt = parser.parse_args(args[1:])
    except:
        print "Error processing arguments!"
        parser.print_help()
        raise

    # help message for wrong district
    help_m_f = '''[WARNING] <District Error> 
There are some useful district choice :
{'''
    help_m_b = "}"

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
    list_county = []
    l_tmp = ""
    
    for line in ts:
        l_tmp = str(line)
        if "CountyID" in l_tmp:
            list_county.append( ( l_tmp.strip(' 0123456789:') + '}' ).replace('\'', '\"') )

    l1 = ""
    for county in list_county:
        if opt.district in county:
            l1 = county

    # if not find this district
    if l1 == "":
        print help_m_f
        for county in list_county:
            l1 = county
            nl = json.loads( l1 )
            print nl['CountyName']['C'], " ,"
        print help_m_b
        return
    
    nl = json.loads( l1 )

    print     "District    : ", nl['CountyName']['C'], " ", nl['CountyName']['E']
    if (not opt.temperature) and (not opt.weather) and (not opt.rain) and (not opt.humidity) :
        print "Temperature : ", nl['Temperature']['C'], "C ", nl['Temperature']['F'], "F"
        print "Weather     : ", nl['Weather']['C'], " ", nl['Weather']['E']
        print "Rain Rate   : ", nl['Rain']['C'], " ", nl['Rain']['E']
        print "Humidity    : ", nl['Humidity'], " %"
    elif opt.temperature:
        print "Temperature : ", nl['Temperature']['C'], "C ", nl['Temperature']['F'], "F"
    elif opt.weather:
        print "Weather     : ", nl['Weather']['C'], " ", nl['Weather']['E']
    elif opt.rain:
        print "Rain (mm)   : ", nl['Rain']['C'], " ", nl['Rain']['E']
    elif opt.humidity:
        print "Humidity    : ", nl['Humidity'], " %"


    print "----- Data from 中央氣象局 -----"
    
    #print(r.history)
    #print(r.url)

    #for line in soup.find_all("span", class_="tem-C is-active"):
    #    print line
    #print soup.find_all("div", class_="tab-content")


if __name__ == '__main__':
   main( sys.argv )
