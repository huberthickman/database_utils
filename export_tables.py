import psycopg2
import sys
import argparse
import os
import os.path
import psycopg2.sql

parser = argparse.ArgumentParser(description='Export all tables to csv from a Postgresql schema')

parser.add_argument('--user', action='store', type=str, required=True)
parser.add_argument('--password', action='store', type=str, required=True)
parser.add_argument('--dbname', action='store', type=str, required=True)
parser.add_argument('--hostname', action='store', type=str, required=True)
parser.add_argument('--port', action='store', type=int, required=True)
parser.add_argument('--dir', action='store', type=str, required=True)

args = parser.parse_args()

os.makedirs(args.dir, exist_ok = True)

print("exporting tables in", args.dbname, "for", args.user)
conn = psycopg2.connect(dbname=args.dbname, user=args.user, 
       password=args.password, 
       host=args.hostname, port=args.port)
cur = conn.cursor()

# Get the list of tables in the schema

schema_sql = """ select table_name from information_schema.tables where table_schema = (%s) """

cur.execute(schema_sql, [args.user])
rs = cur.fetchall()

for t in rs:
    table_name = t[0]
    print("Exporting", table_name)
    filename = os.path.join(args.dir,args.user + "." + table_name + ".csv")
    f = open(filename, 'w')
    #cur.copy_to(f, table_name, sep = "|") f.close()
    rc = cur.copy_expert(
            psycopg2.sql.SQL("copy (select * from {}  ) to STDOUT WITH CSV HEADER").format(psycopg2.sql.Identifier(table_name)), f, size=64000)
    f.close()


