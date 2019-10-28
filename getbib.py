import requests
from bs4 import BeautifulSoup as BS
import time
import sys
import pdb
import os.path as path


def input_error():
    print('      Call this function with author surname, start year and end year respectively.')
    print('      For example:')
    print('      >>>python3 getbib.py Hoeijmakers 2003 2021')
    print('      Providing a path to a bibfile is optional (if not provided, defaults to bib.bib)')
    print('      For example:')
    print('      >>>python3 getbib.py Hoeijmakers 2003 2021 ~/Documents/paper/references.bib')
    sys.exit()

if len(sys.argv) < 4:
    print('Input error: Insufficient arguments provided.')
    input_error()

surname = sys.argv[1].capitalize()
startyear = sys.argv[2]
endyear = sys.argv[3]


if startyear.isdigit() == False or endyear.isdigit() == False:
    print('   Input error: Start and end year should be numbers.')
    input_error()

if len(sys.argv) > 4:
    outbib = sys.argv[4]
else:
    outbib = 'bib.bib'




root = 'http://adsabs.net/cgi-bin/nph-abs_connect?db_key=AST&aut_logic=OR&'
author = 'author=%5E'+surname
start = '&start_mon=&start_year='+str(startyear)
end = '&end_mon=&end_year='+str(endyear)
tail = '&ttl_logic=OR&title=&txt_logic=OR&text=&nr_to_return=2000&start_nr=1&sort=NDATE&jou_pick=ALL'

url = root + author + start + end + tail


ads_html = BS(requests.get(url).content,'html.parser')
rows = ads_html.find_all('tr')

#This is where the output of the reading of the table is parsed into.
bibcode_list = []
authors_list = []
titles_list = []
dates_list = []
for i in range(len(rows)):
    box = rows[i].find('input',attrs={'type':'checkbox'})
    if box is not None:
        #If a checkbox has been found, I know that the next line of the table contain the information that I need.
        bibcode_list.append(box['value'])
        infofields1 = rows[i].find_all('td')
        dates_list.append(infofields1[3].text)
        infofields2 = rows[i+1].find_all('td')
        authors_list.append(infofields2[1].text)
        titles_list.append(infofields2[2].text)


print('')
print('')
if len(bibcode_list) == 0:
    print('No references found.')
    sys.exit()


#Below we do all the output.
for i in range(len(bibcode_list)):
    authors = authors_list[i].split(';')
    outstring = ''
    for j in range(min([3,len(authors)])):
        outstring+=authors[j]+';'

    print(str(i)+')    '+dates_list[i]+'    '+outstring[0:-2]+' et al.')
    print('       '+titles_list[i])
    # print('       '+bibcode_list[i])
    print('')



number = input("Which reference do you want? q for cancel. ")
if number == 'q':
    sys.exit()
if number.isdigit() == False:
    print('Error, please type a number.')
    sys.exit()

target_ref_name = surname+dates_list[int(number)].split('/')[-1]
bibcode = bibcode_list[int(number)]#'2019A&A...627A.165H'
bibtex_root = 'http://adsabs.harvard.edu/cgi-bin/nph-bib_query?bibcode='
bibtex_tail = '&data_type=BIBTEX'
bibtex_url = bibtex_root+bibcode+bibtex_tail
bibtext = BS(requests.get(bibtex_url).content,'html.parser').prettify()
#This is a string.

art_key = '@ARTICLE{'
art_i = bibtext.index(art_key)#Search for where @ARTICLE STARTS. This is the start of our reference.
# print('')
# print('')
# print(bibtext[art_i:-1])#This is the entire remainder of the file produced by ADS.
# print('')
print(target_ref_name)
ref_name = bibtext[art_i:-1].replace('@ARTICLE{','').split(',')[0]#Split before the first comma and remove the @ARTICLE{
#to retrieve the name of the reference.

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
    bibtext_out = bibtext[art_i:-1].replace(ref_name,outname)

    #The following block tests if the reference already exists, and if so, appends a suffix.
    while '@ARTICLE{'+outname+',\n' in content:
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
else:
    bibtext_out = bibtext[art_i:-1].replace(ref_name,target_ref_name)
    with open(outbib,'w') as fp:
        fp.write('\n')
        fp.write(bibtext_out)
        fp.write('\n')
    print('Created new '+outbib+' file and added '+target_ref_name)

print('Finished')

#TO ADD:
#THE ABILITY TO DEAL WITH MULTIPLE REFERENCES AT ONCE.
#THE ABILITY TO ADD INITIALS.
