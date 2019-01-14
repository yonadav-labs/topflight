# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import math

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from .models import *
from .lineup import *

CSV_FIELDS = {
    'FanDuel': ['P', 'C1B', '2B', '3B', 'SS', 'OF', 'OF', 'OF', 'UTIL'],
    'DraftKings': ['P', 'P', 'C' '1B', '2B', '3B', 'SS', 'OF', 'OF', 'OF'],
}

SALARY_CAP = {
    'FanDuel': 35000,
    'DraftKings': 50000,
}

TEAM_MEMEBER_LIMIT = {
    'FanDuel': 5,
    'DraftKings': 6
}

def _get_lineups(request):
    params = json.loads(request.body)
    ids = params.get('ids')
    locked = params.get('locked')
    num_lineups = min(params.get('num_lineups', 1), 150)
    ds = params.get('ds', 'DraftKings')
    min_salary = params.get('min_salary', 0)
    max_salary = params.get('max_salary', SALARY_CAP[ds])
    min_team_member = params.get('min_team_member', 0)
    max_team_member = params.get('max_team_member', TEAM_MEMEBER_LIMIT[ds])
    exposure = params.get('exposure')
    team_stack = params.get('team_stack', {})
    cus_proj = params.get('cus_proj', {})

    ids = [ii for ii in ids if ii]
    flt = { ATTR[ds]['projection']+'__gt': 0, 'id__in': ids }
    players = Player.objects.filter(**flt).order_by('-'+ATTR[ds]['projection'])

    _team_stack = {}
    teams = players.values_list('team', flat=True).distinct()
    for ii in teams:
        if not ii:
            continue
        if ii in team_stack:
            _team_stack[ii] = team_stack[ii]
        else:
            _team_stack[ii] = { 'min': min_team_member, 'max': max_team_member }

    # get exposure for each valid player
    _exposure = []

    for ii in players:
        val = exposure.get(ii.id)
        if not val:
            continue

        _exposure.append({
            'min': int(math.ceil(val['min'] * num_lineups)),
            'max': int(math.floor(val['max'] * num_lineups)),
            'id': ii.id
        })

    return calc_lineups(players, num_lineups, locked, ds, min_salary, max_salary, _team_stack, _exposure, cus_proj)

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
                'draftkings_name_id': jj.dk_id,
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
