# bulkupload-rest
New Version of bulkupload that utilizes the Veracode REST APIs

Utilizes [veracode-api-py by tjarrettveracode](https://github.com/veracode/veracode-api-py) to make bulk changes to objects using calls to the Veracode REST APIs.

Requires a valid credentials file to exist on your system. See the [Veracode Help Center](https://help.veracode.com/r/c_configure_api_cred_file) for more information. You can use multiple profiles within this credentials file, and the script will prompt you for which one you'd like to use.

When prompted, point to a CSV file where the first column contains various parameter names including `apiaction`. Valid `apiaction` values currently include:
  - `updateuser`
  - `resetpassword`
  - `deleteuser`
  - `createteam`