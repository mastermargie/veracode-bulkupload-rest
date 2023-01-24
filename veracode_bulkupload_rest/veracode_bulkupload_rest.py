import csv
import sys
import traceback

try:
    from .logger import Logger
    from .credentials import set_api_creds
    from .updateuser import update_user, reset_user_password
except ImportError:
    from logger import Logger
    from credentials import set_api_creds
    from updateuser import update_user, reset_user_password

from veracode_api_py import Users, Healthcheck, Teams


def credentials_selftest():
    r = Healthcheck().healthcheck()


def delete_user(row):
    guid = get_guid( row.pop('username').lower() )
    r = Users().delete(guid)

    return r


def create_team(row):
    if 'members' in row:
        row['members'] = row.pop('members').split(',')
    r = Teams().create(**row)


def bulkupload(file_loc = None):
    file_loc = file_loc or input('CSV File: ')

    myLogger = Logger(file_loc)
    myLogger.info('NEW RUN BEGINNING')

    set_api_creds()
    try:
        credentials_selftest()
    except:
        myLogger.error("Failed Credentials Test, Quitting...")
        return 0

    with open(file_loc, newline='') as CSVFILE:
        reader = csv.DictReader(CSVFILE)
        filtered = []
        for row in reader:
            filtered.append( {k: v for k, v in row.items() if ((v is not None) and (v.strip() != '')) } )

    for idx, row in enumerate(filtered, 2):
        try:
            if 'apiaction' not in row:
                continue
            apiaction = row.pop('apiaction').strip().lower()
            match apiaction:
                case "updateuser": update_user(row)
                case "resetpassword": reset_user_password( row.get('username') )
                case "deleteuser": delete_user(row)
                case "createteam": create_team(row)
                case _: raise Exception('Row #{}: Invalid apiaction'.format(idx))
            myLogger.info('Row #{}: SUCCESS'.format(idx))
        except Exception as e:
            myLogger.error('Row #{}: {}'.format(idx, e))
            # myLogger.error( traceback.print_exc() )


def main(args):
	bulkupload()
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))