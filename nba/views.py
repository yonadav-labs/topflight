# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import math

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from .models import *
from .lineup import *

POSITION = ['PG', 'SG', 'SF', 'PF', 'C']

CSV_FIELDS = {
    'FanDuel': ['PG', 'PG', 'SG', 'SG', 'SF', 'SF', 'PF', 'PF', 'C'],
    'DraftKings': ['PG', 'SG', 'SF', 'PF', 'C', 'G', 'F', 'UTIL'],
}

SALARY_CAP = {
    'FanDuel': 60000,
    'DraftKings': 50000,
}

TEAM_MEMEBER_LIMIT = {
    'FanDuel': 4,
    'DraftKings': 8
}

def _get_lineups(request):
    params = json.loads(request.body)
    ids = params.get('ids')
    locked = params.get('locked')
    num_lineups = min(params.get('num-lineups', 1), 150)
    ds = params.get('ds', 'DraftKings')
    min_salary = params.get('min_salary', 0)
    max_salary = params.get('max_salary', SALARY_CAP[ds])
    min_team_member = params.get('min_team_member', 0)
    max_team_member = params.get('max_team_member', TEAM_MEMEBER_LIMIT[ds])
    exposure = params.get('exposure')

    flt = { ATTR[ds]['projection']+'__gt': 0, 'id__in': ids }
    players = Player.objects.filter(**flt).order_by('-'+ATTR[ds]['projection'])

    # get exposure for each valid player
    _exposure = []
    for ii in players:
        val = exposure.get(ii.id)
        if not val:
            continue

        _exposure.append({
            'min': int(math.ceil(val['min'] * num_lineups)),
            'max': int(math.floor(val['max'] * num_lineups))            
            'id': ii.id
        })

    return calc_lineups(players, num_lineups, locked, ds, min_salary, max_salary, min_team_member, max_team_member, _exposure)

@csrf_exempt
def gen_lineups(request):
    lineups = _get_lineups(request)

    params = json.loads(request.body)
    ds = params.get('ds')

    header = CSV_FIELDS[ds] + ['Spent', 'Projected']
    
    lineups_ = []
    for ii in lineups:
        players = []
        for jj in ii.get_players():
            players.append({
                'id': jj.id,
                'name': jj.nickname,
                'avg_projection': getattr(jj, ATTR[ds]['projection']),
                'position': getattr(jj, ATTR[ds]['position']),
                'salary': getattr(jj, ATTR[ds]['salary']),
                'team': jj.team,
                'count': get_num_lineups(jj, lineups)
            })

        lineups_.append({ 
            'players': players,
            'salary': ii.spent(),
            'projection': ii.projected()
        })

    result = {
        'lineups': lineups_,
        'ds': ds,
        'total': len(lineups)
    }

    return JsonResponse(result, safe=False)
