# new terminal
# cd spider/downloads
# python mongo_import.py -u 'mongodb+srv://mongodb:HelloWorld2929@mdm-cluster-1.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000' 
# -i '/Users/morenogallo/Desktop/ZHAW/6_Semester/MDM/MDM_Projekt1_Moreno_Gallo/spider/spider/spiders/produkte.json' -d 'produkte' -c 'produkte'


import argparse
import json
import os
from concurrent.futures import ProcessPoolExecutor

from pymongo import MongoClient

#import gpxpy
#import gpxpy.gpx
from pathlib import Path


class JsonLinesImporter:
    def __init__(self, file, mongo_uri, db='produkte', collection='produkte'):
        self.file = file
        self.mongo_uri = mongo_uri
        self.db = db
        self.collection = collection

    def import_to_mongodb(self):
        client = MongoClient(self.mongo_uri)
        db = client[self.db]
        collection = db[self.collection]
        with open(self.file, 'r', encoding='UTF-8') as file:
            for line in file:
                try:
                    document = json.loads(line)
                    collection.insert_one(document)
                except json.JSONDecodeError as e:
                    print(f"Could not decode JSON: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--uri', required=True, help="MongoDB URI with username/password")
    parser.add_argument('-i', '--input', required=True, help="Input file in JSON Lines format")
    parser.add_argument('-d', '--db', required=True, help="Name of the MongoDB database")
    parser.add_argument('-c', '--collection', required=True, help="Name of the MongoDB collection")
    args = parser.parse_args()

    importer = JsonLinesImporter(args.input, args.uri, db=args.db, collection=args.collection)
    importer.import_to_mongodb()
