#!/usr/bin/env python3
try:
    import requests
    from bs4 import BeautifulSoup as BS
except:
    print('Make sure that the following packages are installed:')
    print('requests')
    print('bs4')
import sys
import pdb
import lib.utils as ut
import webbrowser


#==================================================================
#             T H E   D O C U M E N T A T I O N
#==================================================================
#This script is a quick-hand way to query the ads system for
#bibtex references.
#It is called from the command line outside of python as:
#python3 searchads.py [authorname] [optional: startyear] [optional: endyear] [optional: path to bibfile (bib.bib by default)]
#Examples:
#python3 searchads.py Hoeijmakers'
#python3 searchads.py Hoeijmakers 2012'
#python3 searchads.py Hoeijmakers 2012 ~/Documents/paper/references.bib'
#python3 searchads.py Hoeijmakers 2012 2019 ~/Documents/paper/references.bib'
#python3 searchads.py Hoeijmakers ~/Documents/paper/references.bib'
#These examples will query the ads for all references with Hoeijmakers as first author,
#with or without a selection of the time frame between the years 2012 and 2019.

#Note that the first numeral is always assumed to be the start year.
#Providing only the endyear is not possible.

#The script will open the classic adsabs webpage displaying the results.
#==================================================================

#First we check the input for completeness and extract the right strings:
surname,startyear,endyear,outbib = ut.parse_input(sys.argv)
#Then we construct the URL needed to access ADS.
#First we check the input for completeness and extract the right strings:
url = ut.create_ads_url(surname,startyear,endyear)
webbrowser.open_new_tab(url)
