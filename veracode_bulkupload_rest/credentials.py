import os

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

def set_api_creds(api_profile = None):
    try:
        api_profile = api_profile or input("Profile Name: ")
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.expanduser("~"), '.veracode', 'credentials'))
        os.environ['VERACODE_API_KEY_ID'] = config.get(api_profile, 'VERACODE_API_KEY_ID')
        os.environ['VERACODE_API_KEY_SECRET'] = config.get(api_profile, 'VERACODE_API_KEY_SECRET')
    except:
        print('Could not pull credentials')