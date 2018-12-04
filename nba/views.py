# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

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

def _get_lineups(request):
    params = json.loads(request.body)
    ids = params.get('ids')
    locked = params.get('locked')
    num_lineups = min(int(params.get('num-lineups', 1)), 150)
    ds = params.get('ds', 'DraftKings')

    if ids:
        players = Player.objects.filter(id__in=ids) 
    else:
        players = Player.objects.filter(avg_projection_fd__gt=0)

    lineups = calc_lineups(players, num_lineups, locked, ds)
    return lineups, players

@csrf_exempt
def gen_lineups(request):
    lineups, players = _get_lineups(request)

    params = json.loads(request.body)
    ds = params.get('ds')

    header = CSV_FIELDS[ds] + ['Spent', 'Projected']
    
    lineups_ = []
    for ii in lineups:
        lineup = []
        for jj in ii.get_players():
            lineup.append({
                'id': jj.id,
                'name': jj.nickname,
                'avg_projection': getattr(jj, ATTR[ds]['projection']),
                'position': getattr(jj, ATTR[ds]['position']),
                'salary': getattr(jj, ATTR[ds]['salary']),
                'team': jj.team
            })
        lineups_.append(lineup)

    result = {
        'lineups': lineups_,
        'ds': ds
    }

    return JsonResponse(result, safe=False)
