# bulkupload-rest
New Version of bulkupload that utilizes the Veracode REST APIs

Utilizes [veracode-api-py by tjarrettveracode](https://github.com/tjarrettveracode/veracode-api-py) to make bulk changes to objects using calls to the Veracode REST APIs.

Initial version was created solely to update the email addresses of user accounts. This will be updated over time to include the ability to create/update/delete objects such as users, application profiles, and teams.

Requires a valid credentials file to exist on your system. See the [Veracode Help Center](https://help.veracode.com/r/c_configure_api_cred_file) for more information.

When prompted, point to a CSV file where the first column is: `resource,apiaction,username,email_address`
Each following line will represent a different user to update, where:
  - `resource`: must be `user`
  - `apiaction`: must be `update`
  - `username`: the username of the user to be updated
  - `email_address`: the new email address for the user to be changed to