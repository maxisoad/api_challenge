email = 'maxisoad@gmail.com'
token = '3aa0a402c6a241c5bafe36e399f927a3'

SQL_COMPETITION_CODE = 'SELECT id FROM competition WHERE code = "{}";'
SQL_TOTAL_PLAYERS = 'SELECT c.id, count(tp.id_player) FROM competition c JOIN competition_team ct on ct.id_competition = c.id JOIN team_player tp ON tp.id_team = ct.id_team WHERE c.code = "{}" GROUP BY c.id;'

SQL_TEAM_IDS = 'SELECT id FROM team WHERE id IN ({});'
SQL_INSERT_COMPETITION = 'INSERT INTO competition VALUES ({});'
SQL_INSERT_TEAMS = 'INSERT IGNORE INTO team VALUES {};'
SQL_INSERT_PLAYERS = 'INSERT IGNORE INTO player VALUES {};'
SQL_INSERT_COMPETITION_TEAM = 'INSERT IGNORE INTO competition_team(id_competition, id_team) VALUES {};'
SQL_INSERT_TEAM_PLAYER = 'INSERT IGNORE INTO team_player(id_team, id_player) VALUES {};'


class HTTP_CODES:
    OK = {'code': 201, 'message': 'Successfully imported'}
    ALREADY_IMPORTED = {'code': 409, 'message':  'League already imported'}
    NOT_FOUND_ERROR = {'code': 404, 'message': 'Not found'}
    CONNECTION_ERROR = {'code': 504, 'message': 'Server Error'}
    PARAMETER_ERROR = {'code': 400, 'message': 'Bad request'}
    TOTAL_PLAYERS = {'code': 200, 'total': ''}
