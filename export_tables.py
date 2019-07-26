import psycopg2
import pprint
import sys
import argparse


parser = argparse.ArgumentParser(description='Export all tables to csv from a Postgresql schema')

parser.add_argument('--user', action='store', type=str, required=True)
parser.add_argument('--password', action='store', type=str, required=True)
parser.add_argument('--dbname', action='store', type=str, required=True)
parser.add_argument('--hostname', action='store', type=str, required=True)
parser.add_argument('--port', action='store', type=int, required=True)

args = parser.parse_args()

print("exporting tables for ", args.dbname)
conn = psycopg2.connect(dbname=args.dbname, user=args.user, password=args.password, 
       host=args.hostname, port=args.port)
cur = conn.cursor()



