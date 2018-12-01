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
    num_lineups = int(params.get('num-lineups', 5))
    ds = params.get('ds', 'DraftKings')

    ids = [int(ii) for ii in ids]
    locked = [int(ii) for ii in locked]

    # players = Player.objects.filter(id__in=ids)
    players = Player.objects.filter(avg_projection_fd__gt=0)
    lineups = calc_lineups(players, num_lineups, locked, ds)
    return lineups, players

@csrf_exempt
def gen_lineups(request):
    lineups, players = _get_lineups(request)

    params = json.loads(request.body)
    ds = params.get('ds')

    header = CSV_FIELDS[ds] + ['Spent', 'Projected']
    
    rows = [ii.get_csv(ds).strip().split(',')+[int(ii.spent()), ii.projected()]
            for ii in lineups]

    result = {
        'lineups': rows
    }

    return JsonResponse(result, safe=False)
