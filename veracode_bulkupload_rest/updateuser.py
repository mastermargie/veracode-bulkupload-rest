import json

from uuid import UUID

from veracode_api_py import Users, Teams


def get_user(username: str):
    r = Users().get_by_name( username.lower() )
    if len(r) != 1:
        raise Exception( '{} user(s) found when 1 was expected; skipping...'.format( len(r) ) )
    return r[0]        


def get_user_guid(username: str) -> UUID:
    return get_user(username).get('user_id')


def reset_user_password(username: str):
    user_id = get_user(username).get('user_legacy_id')
    Users().reset_password(user_id)


def update_user_email_address(username: str, email_address: str):
    user = get_user(username)
    
    ignore_verification = False
    if 'last_login' not in user:
        ignore_verification = True
    
    r = Users().update_email_address(user.get('user_id'), email_address, ignore_verification)

    if 'last_login' not in user:
        Users().reset_password( user.get('user_legacy_id') )

    if ( r.get('pending_email_address') != email_address ) and ( r.get('email_address') != email_address ):
        raise Exception('Email Change Verification Failure')


def update_user_roles(roles: str) -> [dict]:
    roles = roles.split(',')
    rolelist = []
    for role in roles:
        rolelist.append({"role_name": role})
    return rolelist


def get_team_ids_from_names(teams: str) -> [UUID]:
    teamlist = teams.strip().split(',')
    all_teams = Teams().get_all(all_for_org=True)
    team_ids = [team.get('team_id') for team in all_teams if team.get('team_name') in teamlist]

    if len(team_ids) == 0:
        raise Exception("No valid teams provided")
    
    return team_ids


def update_user_teams(teams: [UUID]) -> [dict]:
    new_teams_list = []
    for team_id in teams:
        new_teams_list.append({"team_id": team_id})
    
    return new_teams_list


def update_user(row: dict):
    username = row.pop('username').lower()
    guid = get_user_guid(username)

    changes = {}

    if 'roles' in row:
        roles = row.pop('roles')
        changes.update({"roles": update_user_roles(roles) })
    
    if 'email_address' in row:
        update_user_email_address(username, row.pop('email_address'))

    if 'allowed_ip_addresses' in row:
        allowed_ip_addresses = row.pop('allowed_ip_addresses').split(',')
        changes.update( {'allowed_ip_addresses': allowed_ip_addresses} )
    
    if 'teams' in row:
        teams = row.pop('teams')
        team_ids = get_team_ids_from_names(teams)
        changes.update( {'teams': update_user_teams(team_ids)} )

    changes.update(row)

    r = Users().update(guid, changes)