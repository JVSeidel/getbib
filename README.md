getbib.py and searchads.py
==========================

This repo contains two scripts that provide a quick-hand way to query the ads system for astronomy papers and
bibtex references.

This helps people who know the papers they want to get from the ADS
and would typically navigate to http://adsabs.net fill in the query form by providing the surname of the first author
like ^Hoeijmakers, optionally add a start or an end year to the search window, press search and then need to navigate
to the appropriate paper; click some more to generate a bibtex reference to finally copy-paste that into a bib.file
on their drive. Well, I certainly got tired of doing that 50 times in a row each time I'm writing a paper, so these two scripts
take the clicking and browsing away from me. It's extra convenient when you are calling LaTeX from the terminal, because you
will already have a terminal window open with a bib file nearby.

If you want to retrieve a bibtex reference and write it to a bibfile real quick, use getbib.py.
If you simply want to search the classical ADS (using the adsabs.net fork) to look up a paper, use searchads.py; which will open a browser window and do the query for you.

The input for both of these works identically:<br>
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

Swap getbib.py with searchads.py if you simply want to search for the references in the browser, e.g.:<br>
*python3 searchads.py Hoeijmakers 2012*<br>

Note that the first numeral is always assumed to be the start year.
Providing only the endyear is not possible.

The script understands initials in a similar way as the ADS query system does, as follows:<br>
*python3 getbib.py Hoeijmakers,H.J. 2003 2031 ~/Documents/paper/references.bib*<br>
Similarly, the script understands compounded surnames if the parts are separated with an underscore, as follows:<br>
*python3 getbib.py de_Mooij,E. 2003 2031 ~/Documents/paper/references.bib*<br>
Careful: No spaces between the parts of the surname, the comma and the initials.
Python understands spaces to delimit different input variables.
The following will return an error:<br>
*python3 getbib.py Hoeijmakers, H.J. 2003 2031 ~/Documents/paper/references.bib*<br>
<br>
getbib.py will return all the references found, and allow the user to select one
or multiple references (separated by comma's), which are to be added to the specified
(or default) bib file.
The script will then query ads for the bibtex reference text, and parse it into the
bibfile, while changing the name to [surname][year] (e.g. Hoeijmakers2018).
If a bibfile with the specified name already exists, the program checks whether
a bibtex reference it is trying to add is already in this bib file. If that is the case,
it will append a lower-case letter to the name of the reference, stating with b.
e.g. Hoeijmakers2018 would become Hoeijmakers2018b if Hoeijmakers2018 already exists.
However, this is not a bibliography manager. The bibtex blocks are added to the file
after another without care of order, and there may be cases where this choice of
naming becomes inconvenient for you. Manual interaction with your bibfile may therefore
still be needed. I may add a certain functionality that orders a bibfile alphabetically
in the future.<br>

**Make it even easier**<br>
...by adding these scripts to your PATH, allowing you to execute them from the
command line from anywhere.<br>
The shebang lines (*#!/usr/bin/env python3*) are already in place, but you may need to customise them for your needs. (The *python3* in this case refers to the alias for your python 3 installation. Call *which python3* to find out the path where the executable is located).<br><br>
To add these scripts to your path:<br>
-Place them (along with the lib folder) in a central directory where you keep the custom routines that you added to your path.<br>
-Make them executable by running *chmod +x getbib.py* and *chmod +x searchads.py*<br>
-Remove the file extension .py for bonus points.<br>
-Open your bash profile located in *~/.bash_profile* or *~/.bashrc* or *~/.zshrc*<br>
-Add the following line at the bottom: *export PYTHON_UTILS="/home/username/wherever_these_codes_are"*, with the correct file path.<br>
-Add the following line: *export PATH="$PYTHON_UTILS:$PATH"*<br>
<br>
Now you should be able to run getbib and searchads from a terminal anywhere, without first needing to call *python3* and without the extension *.py* (if you removed it).<br>
For example, *hoeijmakers$ searchads Hoeijmakers 2012* is now a working command on my system.<br>

**Disclaimer**<br>
If this way of querying or returning references is ever altered by ADS, this code will probably fail to submit the query or parse the resulting html table properly. I take no responsibility
for irreparably damaging your bibfile.
