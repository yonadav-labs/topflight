# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from nba.models import *

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'position', 'team', 'opponent', 'salary', 'dk_salary',
                    'avg_projection_fd', 'avg_projection_dk']
    search_fields = ['first_name', 'last_name', 'team', 'id']
    list_filter = ['team', 'position']

admin.site.register(Player, PlayerAdmin)
