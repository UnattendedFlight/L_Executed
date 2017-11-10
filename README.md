# L_Executed
Lookup executed prisoners in the US from https://deathpenaltyinfo.org/ by 
name, 
race, 
age, 
victims (not victim names), 
date of execution, 
state, 
execution method, 
county, 
and other variables.. 

This also tries to find more information about an individual from http://murderpedia.org/, 
but is not always successful in scraping because of my shitty code..

## Usage
```
python main.py [-h] [-v] [-l] [-p] [-f FORMAT] [term [term ...]]

Look up someone in the US's database of executions..

positional arguments:
  term                  search terms to fullfill

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose
  -l, --verbose-lookup
  -p, --pretty-print    prints results of --format in a easily readable way.
  -f FORMAT, --format FORMAT
                        output format ['dict', 'json_dump', 'list', 'string']
```

## Notice
This is shit i wrote in English class when the topic was execution (moral dilemmas etc..) 
and I thought it would be cool to just type a name and get all this information with python
without having to go through the bulky website. Also, where applicable, it is great to get additional info 
from murderpedia.org in one go.

