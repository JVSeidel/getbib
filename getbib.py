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
import os.path as path
import lib.utils as ut


#==================================================================
#             T H E   D O C U M E N T A T I O N
#==================================================================
#This script is a quick-hand way to query the ads system for
#bibtex references.
#It is called from the command line outside of python as:
#python3 getbib.py [authorname] [optional: startyear] [optional: endyear] [optional: path to bibfile (bib.bib by default)]
#Examples:
#python3 getbib.py Hoeijmakers'
#python3 getbib.py Hoeijmakers 2012'
#python3 getbib.py Hoeijmakers 2012 ~/Documents/paper/references.bib'
#python3 getbib.py Hoeijmakers 2012 2019 ~/Documents/paper/references.bib'
#python3 getbib.py Hoeijmakers ~/Documents/paper/references.bib'
#These examples will query the ads for all references with Hoeijmakers as first author,
#with or without a selection of the time frame between the years 2012 and 2019.

#Note that the first numeral is always assumed to be the start year.
#Providing only the endyear is not possible.

#The script understands initials in a similar way as the ADS query system does, as follows:
#python3 getbib.py Hoeijmakers,H.J. 2003 2031 ~/Documents/paper/references.bib

#The script will return all the references found, and allow the user to select one
#or multiple references (separated by comma's), which are to be added to the specified
#(or default) bib file.
#The script will then query ads for the bibtex reference text, and parse it into the
#bibfile, while changing the name to [surname][year] (e.g. Hoeijmakers2018).
#If a bibfile with the specified name already exists, the program checks whether
#a bibtex reference it is trying to add is already in the bib file. In that case,
#it will append a lower-case letter to the name of the reference, stating with b.
#e.g. Hoeijmakers2018 would become Hoeijmakers2018b.

#If this way of returning references is every altered by ADS, this code will probably fail
#to parse the html table (see below) properly.
#==================================================================



#First we check the input for completeness and extract the right strings:
surname,startyear,endyear,outbib = ut.parse_input(sys.argv)
#Then we start constructing the URL needed to access ADS.
url = ut.create_ads_url(surname,startyear,endyear)
# root = 'http://adsabs.net/cgi-bin/nph-abs_connect?db_key=AST&aut_logic=OR&'
# author = 'author=%5E'+surname
# start = '&start_mon=&start_year='+str(startyear)
# end = '&end_mon=&end_year='+str(endyear)
# tail = '&ttl_logic=OR&title=&txt_logic=OR&text=&nr_to_return=2000&start_nr=1&sort=NDATE&jou_pick=ALL'
# url = root + author + start + end + tail

#Execute the actual query.
ads_html = BS(requests.get(url).content,'html.parser')
#THe result is a massive html table. The following searches it for the relevant information:
rows = ads_html.find_all('tr')#First, select all table rows.
#This is where the output of the reading of the table will parsed into.
bibcode_list = []
authors_list = []
titles_list = []
dates_list = []
for i in range(len(rows)):#Loop through all the rows...
    box = rows[i].find('input',attrs={'type':'checkbox'})#...each reference has a checkbox that can be used as an identifier.
    if box is not None:
        #If a checkbox has been found, I know that the next line of the table contain the information that I need.
        bibcode_list.append(box['value'])
        infofields1 = rows[i].find_all('td')#We need to find field 4 in this row for the month/year of the reference.
        dates_list.append(infofields1[3].text)
        infofields2 = rows[i+1].find_all('td')
        authors_list.append(infofields2[1].text)#We need to find fields 2 and 3 in the next row to find the authors and the paper title.
        titles_list.append(infofields2[2].text)
print('')
print('')
if len(bibcode_list) == 0:
    print('No references found.')
    sys.exit()


#Now we start to handle the output that is printed to screen for the user to be able
#to make a decision what reference(s) to add.
for i in range(len(bibcode_list)):
    authors = authors_list[i].split(';')#ADS separates authors by ;. Convenient.
    outstring = ''
    for j in range(min([3,len(authors)])):#Print up to three co-authors.
        outstring+=authors[j]+';'
    print(str(i)+')    '+dates_list[i]+'    '+outstring[0:-2]+' et al.')
    #the 0:-2 indexing is to get rid of the last trailing ; that was added, and replace it with et al.
    print('       '+titles_list[i])
    print('')
print("Which reference do you want? q for cancel.")
input = input("Separate more than one number with a comma.\n").split(',')#This is split on the , to deal with a sequence of numbers.
#It also works if only one number is provided.
if input[0] == 'q':
    sys.exit()

#To proceed, we first do checks on the input...
for number in input:
    if number.isdigit() == False:#Is it a number?
        print('Error, please provide only numbers. Exiting.')
        sys.exit()
    if int(number) >= len(bibcode_list):
        print('Error, that many reference were not returned.')
        sys.exit()
#...Then the actual functionality.
for number in input:
    target_ref_name = surname.split('%2C+')[0]+dates_list[int(number)].split('/')[-1]
    bibcode = bibcode_list[int(number)]#'2019A&A...627A.165H'
    bibtex_root = 'http://adsabs.harvard.edu/cgi-bin/nph-bib_query?bibcode='
    bibtex_tail = '&data_type=BIBTEX'
    bibtex_url = bibtex_root+bibcode+bibtex_tail
    bibtext = BS(requests.get(bibtex_url).content,'html.parser').prettify()#This is a big string wth line breaks.

    art_key = '@ARTICLE{'
    try:
        art_i = bibtext.index(art_key)#Search for where @ARTICLE STARTS. This is the start of our reference.
    except:
        try:
            art_key = '@INPROCEEDINGS{'
            art_i = bibtext.index(art_key)
        except:
            try:
                art_key = '@MISC{'
                art_i = bibtext.index(art_key)
            except:
                print("Error: The reference you are trying to add is not an ARTICLE,")
                print("INPROCEEDINGS OR MISC. Sorry, you need to add it manually.")
                sys.exit()
    ref_name = bibtext[art_i:-1].replace(art_key,'').split(',')[0]#Split before the first comma and remove the @ARTICLE{
    #to retrieve the current name of the reference. Which can be garbled, and which we dont want to use in LaTeX.
    suffix=['','b','c','d','e','f','g','h','i','j','k']#These are the possible suffixes that can be added to the reference to distinguish it from
    #duplicate references, e.g. Hoeijmakers2018 exists? Then we add Hoeijmakers2018b.
    #The first one is reserved for the existing reference. Hoeijmakers2018a is never added by this program.
    #It either already exists, or it is not necessary.
    #If Hoeijmakers2018a exists but Hoeijmakers2018 doesn't, this code will add you Hoeijmakers2018.
    #Its up to you to manage your bibtex file properly.
    if path.isfile(outbib):
        print(outbib+' exists. The reference will be appended.')
        with open(outbib) as fp:
            content=fp.readlines()
        i=0
        outname=target_ref_name+suffix[i]
        bibtext_out = bibtext[art_i:-1].replace(ref_name,outname)#Swap the garbled name for the intelligble name.
        #The following block tests if the reference already exists, and if so, swaps for a suffixed-version of the name instead.
        while art_key+outname+',\n' in content:
            print('   '+outname+' already existed.')
            i+=1
            if i > len(suffix)-1:
                print('ERROR: Too many references called '+target_ref_name+' already present in the bibfile.')
                print('Please go add this reference manually:')
                print(bibtext[art_i:-1].replace(ref_name,target_ref_name))
            outname=target_ref_name+suffix[i]
            print('   Changing to '+outname)
            bibtext_out = bibtext[art_i:-1].replace(ref_name,outname)
        with open(outbib, 'a') as fp:
            fp.write('\n')
            fp.write(bibtext_out)
            fp.write('\n')
        print('Added reference '+outname+' to '+outbib)
    else:#else, if the file didn't exist:
        bibtext_out = bibtext[art_i:-1].replace(ref_name,target_ref_name)
        with open(outbib,'w') as fp:
            fp.write('\n')
            fp.write(bibtext_out)
            fp.write('\n')
        print('Created new '+outbib+' file and added '+target_ref_name)
