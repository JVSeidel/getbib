getbib.py and searchads.py
==========================

This repo contains two scripts that provide a quick-hand way to query the ads system for astronomy papers and
bibtex references.

This helps people who know the papers they want to get from the ADS
and would typically navigate to http://adsabs.net fill in the query form by providing the surname of the first author
like ^Hoeijmakers, optionally add a start or an and end year to the search window, press search and then need to navigate
to the appropriate paper, and click some more to generate a bibtex reference to finally copy-paste that into a bib.file
on their drive. Well, I certainly got tired of doing that 50 times in a row each time I'm writing a paper, so these two scripts
take the clicking and browsing away from me. It's extra convenient when you are calling LaTeX from the terminal, because you
will already have a terminal window open with a bib file nearby.

If you want to retrieve a bibtex reference and write it to a bibfile real quick, use getbib.py.
If you simply want to search the classical ADS (using the adsabs.net fork) to look up a paper, use searchads.py.

The input for both of these works identical:<br>
Each script is called from the command line (in bash, outside of python) as:<br>
*python3 getbib.py [authorname] [optional: startyear] [optional: endyear] [optional: path to ibfile (bib.bib by default)]*<br>
Examples:<br>
*python3 getbib.py Hoeijmakers*<br>
*python3 getbib.py Hoeijmakers 2012*<br>
*python3 getbib.py Hoeijmakers 2012 ~/Documents/paper/references.bib*<br>
*python3 getbib.py Hoeijmakers 2012 2019 ~/Documents/paper/references.bib*<br>
*python3 getbib.py Hoeijmakers ~/Documents/paper/references.bib*<br>
These examples will query the ads for all references with Hoeijmakers as first author,
with or without a selection of the time frame between the years 2012 and 2019.

Swap getbib.py with searchads.py if you simply want to search for the references in the rowser, e.g.:<br>
*python3 searchads.py Hoeijmakers 2012*<br>

Note that the first numeral is always assumed to be the start year.
Providing only the endyear is not possible.

The script understands initials in a similar way as the ADS query system does, as follows:<br>
*python3 getbib.py Hoeijmakers,H.J. 2003 2031 ~/Documents/paper/references.bib*
Careful: No spaces between the surname, the comma and the initials.
Python understands spaces to delimit different input variables.

getbib.py will return all the references found, and allow the user to select one
or multiple references (separated by comma's), which are to be added to the specified
(or default) bib file.
The script will then query ads for the bibtex reference text, and parse it into the
bibfile, while changing the name to [surname][year] (e.g. Hoeijmakers2018).
If a bibfile with the specified name already exists, the program checks whether
a bibtex reference it is trying to add is already in the bib file. In that case,
it will append a lower-case letter to the name of the reference, stating with b.
e.g. Hoeijmakers2018 would become Hoeijmakers2018b.

If this way of querying or returning references is ever altered by ADS, this code will probably fail
to submit the query or parse the resulting html table properly.
