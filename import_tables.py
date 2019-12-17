#
# Import a sheet from an Excel workbook page into a sqlite database.
# The table name is the sheet name.
#
import sqlite3
import argparse
import pandas
import sys

print(sys.argv)
parser = argparse.ArgumentParser(description='Import a page in an Excel workbook into a sqlite databases')

parser.add_argument('--dbfilename', action='store', type=str, required=True)
parser.add_argument('--excel_file_name', action='store', type=str, required=True)
parser.add_argument('--sheetname', action='store', type=str, required=True)

args = parser.parse_args()

con = sqlite3.connect(args.dbfilename)
cur = con.cursor()

df = pandas.read_excel(args.excel_file_name, sheet_name=args.sheetname)
df.columns = [c.replace(' ', '_').replace('(', '_').replace(')', '').replace('/', '_').lower() for c in df.columns]

table_name = args.sheetname.lower().replace('-', '_').replace(' ', '_')
print('Table name is ' + table_name)

df.to_sql(table_name, con=con, if_exists='replace')

con.close()
