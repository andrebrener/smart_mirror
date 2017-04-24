# =============================================================================
#          File: test.py
#        Author: Andre Brener
#       Created: 22 Apr 2017
# Last Modified: 24 Apr 2017
#   Description: description
# =============================================================================
import json

from datetime import date, timedelta

import pandas as pd
import http.client


def get_competition(link):
    return link['competition']


def get_home_goals(result):
    return result['goalsHomeTeam']


def get_away_goals(result):
    return result['goalsAwayTeam']


def get_home_odds(odds):
    if odds:
        return odds['homeWin']


def get_draw_odds(odds):
    if odds:
        return odds['draw']


def get_away_odds(odds):
    if odds:
        return odds['awayWin']


def get_team_id(team_dict):
    val = team_dict['self']['href']
    rv = val.rsplit('/', 1)[-1]
    return rv


def get_teams(connection, headers, comps):
    for comp in comps:
        url = '/v1/competitions/{}/teams'.format(comp)
        connection.request('GET', url, None, headers)
        response = json.loads(connection.getresponse().read().decode())

        df = pd.DataFrame(response['teams'])
        df['id'] = df['_links'].apply(get_team_id)
        # print(df.head())
        df = df[['id', 'code', 'name']]
        df.to_csv('preferred_teams_{}.csv'.format(comp), index=False)


def get_fixture(connection, headers, url, days_past=30, days_next=30):

    connection.request('GET', url, None, headers)
    response = json.loads(connection.getresponse().read().decode())

    df = pd.DataFrame(response['fixtures'])

    data_functions = {
        'competition': ('_links', get_competition),
        'home_goals': ('result', get_home_goals),
        'away_goals': ('result', get_away_goals),
        'home_odds': ('odds', get_home_odds),
        'draw_odds': ('odds', get_draw_odds),
        'away_odds': ('odds', get_away_odds)
    }

    for key, val in data_functions.items():
        df[key] = df[val[0]].apply(val[1])

    df['date'] = pd.to_datetime(
        df['date']).dt.tz_localize('utc').dt.tz_convert('America/Araguaina')

    today = date.today()
    df = df[(df['date'] >= today - timedelta(days_past)) &
            (df['date'] <= today + timedelta(days_past))]

    for col in ['away_goals', 'home_goals']:
        df[col].fillna('-', inplace=True)

    return df


def show_results(connection, headers, comp_df, chosen_teams):
    for comp_id in comp_df['id']:
        comp_name = comp_df[comp_df['id'] == comp_id]['caption'].iloc[0]
        url = '/v1/competitions/{}/fixtures'.format(comp_id)
        fixture_df = get_fixture(
            connection, headers, url, days_next=4, days_past=3)
        fixture_df = fixture_df[(fixture_df['homeTeamName'].isin(
            chosen_teams)) | (fixture_df['awayTeamName'].isin(chosen_teams))]
        if not fixture_df.empty:
            print('\n', comp_name, '\n')
            for row in range(fixture_df.shape[0]):
                d = fixture_df.iloc[row]
                string_date = d['date'].strftime('%a, %b %d  %H.%M hs')
                hg = ''
                ag = ''
                if d['away_goals'] != '-':
                    hg = int(d['home_goals'])
                    ag = int(d['away_goals'])
                print('{}  {}    {} {} - {} {}'.format(string_date, d[
                    'status'], d['homeTeamName'], hg, ag, d['awayTeamName']))


if __name__ == '__main__':

    data_file = open('football_api_key.txt', 'r')
    key = data_file.read().strip()
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': key, 'X-Response-Control': 'full'}
    team = 5
    team_url = '/v1/teams/{}/fixtures'.format(team)
    # get_fixture(connection, headers, url)

    comp_url = '/v1/competitions/'

    leagues = pd.read_csv('preferred_leagues.csv')
    teams = pd.read_csv('preferred_teams.csv')

    # print(leagues.head())

    comps = leagues['id'].unique()
    team_names = teams['name'].unique()

    show_results(connection, headers, leagues, team_names)
