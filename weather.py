#!/usr/bin/env python
# -*- encoding: utf8-*-

import requests
from bs4 import BeautifulSoup
import subprocess
import sys
import argparse
import json


def weather( args ):

    parser = argparse.ArgumentParser("parse!");
    
    parser.add_argument( '-d', '--district', dest='district', default='Taipei City', type=str )
    parser.add_argument( '-t', '--timerange', dest='timerange', default=1, type=int )

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

### request! ###
    url1 = "https://www.cwb.gov.tw/Data/js/TableData_36hr_County_C.js"
    url2 = "https://www.cwb.gov.tw/Data/js/info/Info_County.js"       # used as the countys' name and their No.
    r = requests.get( url1, allow_redirects=False )
    r2 = requests.get( url2, allow_redirects=False )
    r.encoding = 'utf8'         # for encoding chinese
    r2.encoding = 'utf8'
    if r.status_code != 200 or r2.status_code != 200:
        print "fail in requesting"
        return 
    #soup = BeautifulSoup(r.text, 'html.parser')

### make county No. dict ###
    county_No_C = {}  # a dictionary (chinese)
    county_No_E = {}  # a dictionary (english)

    ts2 = (r2.text).split('\n')

    lst_json = []
    for line in ts2:
        if ("{" in line) and ("}" in line):
            lst_json.append( json.loads( line.strip(" ,;").replace('\'','\"') ) )

    for js in lst_json:
        county_No_C[ js['Name']['C'].decode('utf-8') ] = js['ID']
        county_No_E[ js['Name']['E'] ] = js['ID']


    #print county_No_C['新北市'.decode('utf-8')]       #for test


### read and make info. json ###
    ts = (r.text).split('\n')

    json_str = ""
    for line in ts:
        if ("var" in line) or ("Var" in line):
            continue
        json_str = json_str + line
    json_str = (("{" + json_str).strip("; ")).replace('\'','\"')
    county_dict = json.loads(json_str)

###  City Name things ###
    
    countyNo = ""
    if (opt.district).replace(' ', '').encode( 'UTF-8' ).isalpha():
        # if it's true, there are just eng alphabet in this string
        # space in the string may made it incorrectly distinguish, so replace(...)
        countyNo = county_No_E.get(opt.district)
    else:
        countyNo = county_No_C.get(opt.district.decode('utf-8'))
        # use get() instead of [] can return None if we can't find corresponding key in this dict with this input

    if countyNo == None:
        print help_m_f,

        for item in county_No_C.items():
            print item[0], ",",
        for item in county_No_E.items():
            print item[0], ",",

        print "\b\b", help_m_b
        return

    C_Dis = ""
    E_Dis = ""

    for item in county_No_C.items():
        if item[1] == countyNo:
            C_Dis = item[0]
    for item in county_No_E.items():
        if item[1] == countyNo:
            E_Dis = item[0]

### print result ###

    print "District    : ", C_Dis, "/", E_Dis
    print "Time Range  : ", county_dict[ countyNo ][opt.timerange]['TimeRange']
    print "Temp. Range : ", county_dict[ countyNo ][opt.timerange]['Temp']['C']['L'], "~" ,county_dict[ countyNo ][opt.timerange]['Temp']['C']['H'], "degree (Celsius)"
    print "Rain Rate   : ", county_dict[ countyNo ][opt.timerange]['PoP'], "%"
    print "Condition   : ", county_dict[ countyNo ][opt.timerange]['Wx']
    
    print "----- Data from 中央氣象局 -----"

    return int(county_dict[ countyNo ][opt.timerange]['PoP'])
    
if __name__ == '__main__':
   weather( sys.argv )
