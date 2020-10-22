from flask.blueprints import Blueprint
from football_data import FootballData
from flask import jsonify
from constants import HTTP_CODES


api = Blueprint('api', __name__, url_prefix='/')


def response(res):
    return jsonify(res), res['code']


@api.route("/import-league/<league>", methods=['GET'])
def import_league(league):
    res = HTTP_CODES.PARAMETER_ERROR
    if league.isalnum():
        fb_data = FootballData()
        res = fb_data.import_league(league.upper())
    return response(res)


@api.route("/total-players/<league>", methods=['GET'])
def total_players(league):
    res = HTTP_CODES.PARAMETER_ERROR
    if league.isalnum():
        fb_data = FootballData()
        total = fb_data.get_total_players(league.upper())
        res = HTTP_CODES.NOT_FOUND_ERROR
        if total != 0:
            res = HTTP_CODES.TOTAL_PLAYERS
            res['total'] = total
    return response(res)
