#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collections import namedtuple
import json
import sys
import csv

"""
    Ce fichier convertit les données brutes de bureaux provenant de
    caen.fr/ResultatsAffichage/MenuScrutin.aspx en format lisible par le scrit Leaflet dans index.hmtl
"""
candidates = ['duron','bruneau', 'NULS']

OfficeResults = namedtuple(
    'OfficeResult',
    ' ,'.join(candidates))

if __name__ == '__main__':

    if len(sys.argv) != 3:
        msg = 'Usage : {command} <input.json> <output.json>'.format(
            command=sys.argv[0])
        print(msg)
        exit()

    offices = {}
    
    # Concert CSV to JSON
    csvfile = open(sys.argv[1], 'r')
    jsonfile = open('tempo.json', 'w')
    fieldnames = ('bureau','sous_bureau','duron','bruneau','NULS')
    reader = csv.DictReader( csvfile, fieldnames, delimiter=';', quotechar='|')
    reader.next() # skip header
    jsonfile.write('{"version":"1", "data":[')
    virg = ''
    for row in reader:
        jsonfile.write('%s' % (virg))
        json.dump(row, jsonfile)
        virg = ',\n'
    jsonfile.write(']}')
    jsonfile.close()
    
    # process data
    with open('tempo.json', 'r') as json_file:
        reader = json.load(json_file, encoding='utf8')
        
        for row in reader['data']:
            # Get results for each political list
            results = sorted(
                [{candidate.lower(): float(row[candidate])}
                 for candidate in candidates],
                key=lambda k: k.values(),
                reverse=True)
            bureau = row['sous_bureau'].split()[0]
            offices[bureau] = results
            pass
        
    with open(sys.argv[2], 'w') as outfile:
        outfile.write('var results = ')
        response_json = json.dump(offices, outfile)
        