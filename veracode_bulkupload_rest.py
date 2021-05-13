import csv, sys, os, json

import logger
from pprint import pprint
from veracode_api_py import Users

def update_user(row):
    r = Users().get_by_name(row.pop('username'))
    if len(r) == 1:
        guid = r[0].get('user_id')
    user_def = json.dumps( {'email_address': row.pop('email_address')} )
    r = Users().update(guid, user_def)
    pprint(Users().get(guid))

def bulkupload(file_loc = None):
    file_loc = file_loc or input('CSV File: ')
    
    myLogger = logger.Logger(file_loc)

    with open(file_loc, newline='') as CSVFILE:
        reader = csv.DictReader(CSVFILE)
        filtered = []
        for row in reader:
            filtered.append( {k: v for k, v in row.items() if ((v is not None) and (v.strip() != '')) } )

    for idx, row in enumerate(filtered, 2):
        if ('resource' in row) and ('apiaction' in row):
            resource = row.pop('resource').strip().lower()
            apiaction = row.pop('apiaction').strip().lower()
            if resource == 'user':
                if apiaction == 'update':
                    update_user(row)
                    myLogger.info('Row #{}: SUCCESS'.format(idx))
                else:
                    myLogger.error('Row #{}: Invalid apiaction'.format(idx))
            else:
                myLogger.error('Row #{}: Invalid resource'.format(idx))

def main(args):
	bulkupload('./test/emailtest.csv')
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))