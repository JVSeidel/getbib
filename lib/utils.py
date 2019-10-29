def input_error():
    import sys
    print('      Call this function with author surname, and optionally a start year and end year respectively.')
    print('      If using getbib, optionally you may also specify a bibfile to which the reference is output.')
    print('      The following are examples of valid input:')
    print('')
    print('      >>>python3 getbib.py Hoeijmakers')
    print('      >>>python3 getbib.py Hoeijmakers 2012')
    print('      >>>python3 getbib.py Hoeijmakers 2015 ~/Documents/paper/references.bib')
    print('      >>>python3 getbib.py Hoeijmakers 2015 2018 ~/Documents/paper/references.bib')
    print('      >>>python3 getbib.py Hoeijmakers ~/Documents/paper/references.bib')
    print('      (If using searchads.py, the above examples work by swapping getbib.py)')
    sys.exit()


def parse_input(arguments):
    """This checks the input that is provided with the call of searchads and getbib.by
    in the command line.
    Input: sys.argv
    Output: The author name, start and end year with which ads will be queried,
    as well as the optional filename for the bibfile (in the case of getbib)"""

    if len(arguments) < 2 :
        print('Input error: Insufficient arguments provided.')
        input_error()
    if len(arguments) > 5:
        print('Input error: Too many arguments provided.')
        input_error()
    if arguments[1].isdigit():
        print('Input error: The first argument should be a name (not a number).')
        input_error()
    surname = arguments[1].capitalize().replace(',','%2C+')
    startyear = '1'
    endyear = '9999'#If ADS remains unchanged for the next 8000 years this will be a problem.
    outbib = 'bib.bib'

    if len(arguments) == 3:#Then we have only a startyear or the filename.
        if arguments[2].isdigit():
            startyear = arguments[2]
        else:
            outbib = arguments[2]
    if len(arguments) == 4:#Then we certainly have the start year and the endyear or the filename.
        startyear = arguments[2]
        if arguments[3].isdigit():
            endyear = arguments[3]
        else:
            outbib = arguments[3]
    if len(arguments) == 5: #Then we have all three.
        startyear = arguments[2]
        endyear = arguments[3]
        outbib = arguments[4]


    if startyear.isdigit() == False or endyear.isdigit() == False:
        print('   Input error: Start and end year should be numbers.')
        input_error()
    return(surname,startyear,endyear,outbib)


def create_ads_url(surname,startyear,endyear):
    root = 'http://adsabs.net/cgi-bin/nph-abs_connect?db_key=AST&aut_logic=OR&'
    author = 'author=%5E'+surname
    start = '&start_mon=&start_year='+str(startyear)
    end = '&end_mon=&end_year='+str(endyear)
    tail = '&ttl_logic=OR&title=&txt_logic=OR&text=&nr_to_return=2000&start_nr=1&sort=NDATE&jou_pick=ALL'
    return(root + author + start + end + tail)
