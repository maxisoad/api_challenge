from database import db
import sqlalchemy.orm as orm
from sqlalchemy import exc
from constants import (SQL_TEAM_IDS, SQL_INSERT_COMPETITION, SQL_INSERT_TEAMS,
                       SQL_INSERT_PLAYERS, SQL_INSERT_COMPETITION_TEAM,
                       SQL_INSERT_TEAM_PLAYER)


def remove_last_comma(command):
    """Remove last comma from command

    Arguments:
        command - plain sql
    """
    return command[:-2]+command[-1:]


def import_to_db(league):
    """Import all the data to the database

    Arguments:
        league - dict with all data
    """
    competition = SQL_INSERT_COMPETITION.format('{},"{}","{}","{}"'.format(
        league['id'], league['name'], league['code'], league['area']['name']))
    values_t = values_s = values_ct = values_tp = ''
    for team in league['teams']:
        # team table, already imported are omited before
        values_t += '({},"{}","{}","{}","{}","{}"),'.format(
            team['id'], team['name'], team['tla'], team['shortName'],
            team['area']['name'], team['email'])
        # competition team table
        values_ct += "({},{}),".format(league['id'], team['id'])
        # if squad comes empty, is because the team is already imported
        # but this also happen because of the use of the free account
        if 'squad' in team.keys():
            for squad in team['squad']:
                values_s += '({},"{}","{}","{}","{}","{}"),'.format(
                    squad['id'], squad['name'], squad['position'],
                    squad['dateOfBirth'][:10], squad['countryOfBirth'],
                    squad['nationality'])
                values_tp += "({},{}),".format(team['id'], squad['id'])
    teams = remove_last_comma(SQL_INSERT_TEAMS.format(values_t))
    competition_team = remove_last_comma(SQL_INSERT_COMPETITION_TEAM.format(values_ct))
    players = team_player = ''
    if values_s != '':
        players = remove_last_comma(SQL_INSERT_PLAYERS.format(values_s))
        team_player = remove_last_comma(SQL_INSERT_TEAM_PLAYER.format(values_tp))
    execute_import(competition+teams+competition_team+players+team_player)


def execute_import(sql):
    """Execute the import

    Arguments:
        sql - complete plain sql
    """
    Session = orm.sessionmaker(bind=db.engine)
    session = Session()
    try:
        session.execute(sql)
    except exc.IntegrityError:
        session.rollback()
    session.commit()
    session.close()
