import http.client
import json
from constants import (token, SQL_COMPETITION_CODE, SQL_TEAM_IDS,
                       SQL_TOTAL_PLAYERS, HTTP_CODES)
from time import sleep
from importer import import_to_db
from database import db


class FootballData():

    COMPETITIONS = '/v2/competitions/{}'
    TEAMS = '/v2/competitions/{}/teams'
    TEAM = '/v2/teams/{}'

    def __init__(self):
        """Constructor, creates connection"""
        self.connection, self.headers = self.get_connection()

    def get_connection(self):
        """Establish connection"""
        connection = http.client.HTTPConnection('api.football-data.org')
        headers = {'X-Auth-Token': token}
        return connection, headers

    def request(self, url, method='GET'):
        """Request to football API

        Arguments:
            url - url to get competitions, teams or squad
        """
        self.connection.request(method, url,
                                None, self.headers)
        response = json.loads(self.connection.getresponse().read().decode())
        print(response)
        return response

    def get_data(self, url):
        response = {'errorCode': 999}
        while 'errorCode' in response.keys():
            print('retry connection')
            response = self.request(url)
        return response

    def import_league(self, code):
        """Get all data from football API

        Arguments:
            code - league code
        """
        res = False
        id_teams = []
        print(code)
        imported = self.competition_imported(code)
        if imported:
            return HTTP_CODES.ALREADY_IMPORTED
        league = self.get_competition(code)
        if 'errorCode' in league.keys():
            res = HTTP_CODES.CONNECTION_ERROR
        elif 'error' in league.keys():
            res = HTTP_CODES.NOT_FOUND_ERROR
        else:
            try:
                teams = self.get_teams(league['id'])
                id_teams = [t['id'] for t in teams['teams']]
                league['teams'] = teams['teams']
                inserted_teams = self.already_inserted_teams(id_teams)
                print(type(inserted_teams))
                for i, team in enumerate(league['teams']):
                    # only do the request if the team is not in the database
                    print('id {} - {}'.format(team['id'], inserted_teams))
                    if int(team['id']) not in inserted_teams:
                        print('peticion {}'.format(team['id']))
                        squad = self.get_team(team['id'])
                        league['teams'][i]['squad'] = squad['squad']
                        # get 5 only for demonstration purposes,
                        # with the free api access, the restriction is 10 request per minute
                        if i > 5:
                            break
                try:
                    import_to_db(league)
                    res = HTTP_CODES.OK
                except Exception as e:
                    res = HTTP_CODES.NOT_FOUND_ERROR
            except Exception as e:
                res = HTTP_CODES.CONNECTION_ERROR
        return res

    def get_competition(self, code):
        """Get competition from football API

        Arguments:
            code - league code
        """
        response = self.request(self.COMPETITIONS.format(code))
        return response

    def get_teams(self, id_league):
        """Get teams from football API

        Arguments:
            id_league - league id
        """
        response = self.request(self.TEAMS.format(id_league))
        return response

    def get_team(self, id_team):
        """Get squad (and other data from the team) from football API

        Arguments:
            id_team - team id
        """
        response = self.request(self.TEAM.format(id_team))
        return response

    def get_total_players(self, code):
        """Total players by league code

        Arguments:
            code - league code
        """
        res = 0
        sql = SQL_TOTAL_PLAYERS.format(code)
        query = db.engine.execute(sql)
        result = query.fetchone()
        if result:
            res = result[1]
        return res

    def already_inserted_teams(self, id_teams):
        """Returns already inserted teams

        Arguments:
            id_teams - array with teams that belongs to a league
        """
        sql = SQL_TEAM_IDS.format(str(id_teams)[1:-1])
        query = db.engine.execute(sql)
        return [r[0] for r in query.fetchall()]

    def competition_imported(self, code):
        """Check if competition exists

        Arguments:
            code - league code
        """
        res = False
        sql = SQL_COMPETITION_CODE.format(code)
        query = db.engine.execute(sql)
        result = query.fetchone()
        if result:
            res = True
        return res
