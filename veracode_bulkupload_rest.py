import csv, sys, os, json, traceback

import logger
from pprint import pprint
from veracode_api_py import Users

def update_user(row):
    r = Users().get_by_name(row.pop('username'))
    if len(r) != 1:
        raise Exception( '{} user(s) found when 1 was expected; skipping...'.format( len(r) ) )
    guid = r[0].get('user_id')
    user_def = {'email_address': row.pop('email_address')}
    r = Users().update(guid, user_def)
    r = Users().get(guid)
    if r.get('pending_email_address') != user_def.get('email_address'):
        raise Exception('Pending Email Check Failed')
    return 0

def bulkupload(file_loc = None):
    file_loc = file_loc or input('CSV File: ')
    
    myLogger = logger.Logger(file_loc)

    with open(file_loc, newline='') as CSVFILE:
        reader = csv.DictReader(CSVFILE)
        filtered = []
        for row in reader:
            filtered.append( {k: v for k, v in row.items() if ((v is not None) and (v.strip() != '')) } )

    for idx, row in enumerate(filtered, 2):
        try:
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
        except Exception as e:
            myLogger.error('Row #{}: {}'.format(idx, e))

def main(args):
	bulkupload('./test/00396829.csv')
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))