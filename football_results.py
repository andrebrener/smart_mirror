# =============================================================================
#          File: test.py
#        Author: Andre Brener
#       Created: 22 Apr 2017
# Last Modified: 27 May 2017
#   Description: description
# =============================================================================
import json
import pickle
import logging
import logging.config

from datetime import date, timedelta

import pandas as pd
import http.client

from config import config

logger = logging.getLogger('main_logger')


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


def tune_goals(goals):
    if goals != '':
        return str(int(goals))
    else:
        return ''


def rename_game_status(status):
    if status.lower() == 'finished':
        return 'FT'
    elif status.lower() == 'in_play':
        return 'LIVE'
    elif status.lower() == 'timed':
        return ''
    else:
        return status


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
            (df['date'] <= today + timedelta(days_next))]

    for col in ['away_goals', 'home_goals']:
        df[col].fillna('', inplace=True)
        df[col] = df[col].apply(tune_goals)

    return df


def get_teams_fixture(connection, headers, comp_df, chosen_teams):
    df_list = []
    for comp_id in comp_df['id'].unique():
        comp_name = comp_df[comp_df['id'] == comp_id]['caption'].iloc[0]
        url = '/v1/competitions/{}/fixtures'.format(comp_id)
        try:
            fixture_df = get_fixture(
                connection, headers, url, days_next=4, days_past=1)
            logger.info("Got Data for {}".format(comp_name))

        except Exception as e:
            logger.error(str(e))
            raise

        fixture_df = fixture_df[(fixture_df['homeTeamName'].isin(
            chosen_teams)) | (fixture_df['awayTeamName'].isin(chosen_teams))]
        fixture_df['competition'] = comp_name
        df_list.append(fixture_df)
    final_df = pd.concat(df_list)
    final_df.sort_values(['date', 'competition'], ascending=True, inplace=True)
    final_df.reset_index(inplace=True)
    final_df['day'] = final_df['date'].dt.strftime('%a, %b %d')
    final_df['time'] = final_df['date'].dt.strftime('%H:%M')
    final_df['status'] = final_df['status'].apply(rename_game_status)
    return final_df


def get_final_dict(df):
    dates_dict = {}
    for d in df['day'].unique():
        grp_df = df[df['day'] == d]
        games_list = get_games_list(grp_df)
        dates_dict[d] = games_list

    return dates_dict


def get_games_list(df):
    games_list = []
    for row in range(df.shape[0]):
        i = df.iloc[row]
        game_data = (i['day'], i['time'], i['competition'], i['homeTeamName'],
                     i['home_goals'], '-', i['away_goals'], i['awayTeamName'],
                     i['status'])
        games_list.append(game_data)
    return games_list


def get_football_data(connection, headers, leagues, team_names):

    fixtures = get_teams_fixture(connection, headers, leagues, team_names)
    games_list = get_games_list(fixtures)

    return games_list


def save_games(games_list, file_name='football_data.pkl'):
    with open(file_name, 'wb') as f:
        pickle.dump(games_list, f)
    logger.info("File Saved as {}".format(file_name))


if __name__ == '__main__':

    logging.config.dictConfig(config['logger'])

    data_file = open('football_api_key.txt', 'r')
    key = data_file.read().strip()
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': key, 'X-Response-Control': 'full'}

    leagues = pd.read_csv('preferred_leagues.csv')
    teams = pd.read_csv('preferred_teams.csv')
    team_names = teams['name'].unique()

    games_list = get_football_data(connection, headers, leagues, team_names)

    save_games(games_list)
