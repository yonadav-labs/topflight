from __future__ import unicode_literals

from django.db import models

ATTR = {
    'FanDuel': {
        'projection': 'fd_projection',
        'salary': 'salary',
        'position': 'position'
    },
    'DraftKings': {
        'projection': 'dk_projection',
        'salary': 'dk_salary',
        'position': 'draftkings_position'
    }
}


class Player(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=12)
    position = models.CharField(db_column='Position', max_length=5, blank=True, null=True)
    first_name = models.CharField(db_column='First_Name', max_length=12, blank=True, null=True)
    nickname = models.CharField(db_column='Nickname', max_length=25, blank=True, null=True)
    last_name = models.CharField(db_column='Last_Name', max_length=25, blank=True, null=True)
    fppg = models.DecimalField(db_column='FPPG', max_digits=12, decimal_places=2, blank=True, null=True)
    played = models.IntegerField(db_column='Played', blank=True, null=True)
    salary = models.IntegerField(db_column='Salary', blank=True, null=True)
    game = models.CharField(db_column='Game', max_length=12, blank=True, null=True)
    team = models.CharField(db_column='Team', max_length=5, blank=True, null=True)
    opponent = models.CharField(db_column='Opponent', max_length=5, blank=True, null=True)
    dk_salary = models.IntegerField(db_column='DK_Salary', blank=True, null=True)
    draftkings_position = models.CharField(db_column='DK_Position', max_length=45, blank=True, null=True)
    dk_id = models.IntegerField(db_column='DK_ID', blank=True, null=True)
    base_1_fd = models.DecimalField(db_column='Base_1_FD', max_digits=12, decimal_places=2, blank=True, null=True)
    base_2_fd = models.DecimalField(db_column='Base_2_FD', max_digits=12, decimal_places=2, blank=True, null=True)
    base_3_fd = models.DecimalField(db_column='Base_3_FD', max_digits=12, decimal_places=2, blank=True, null=True)
    base_4_fd = models.DecimalField(db_column='Base_4_FD', max_digits=12, decimal_places=2, blank=True, null=True)
    base_1_dk = models.DecimalField(db_column='Base_1_DK', max_digits=12, decimal_places=2, blank=True, null=True)
    base_2_dk = models.DecimalField(db_column='Base_2_DK', max_digits=12, decimal_places=2, blank=True, null=True)
    base_3_dk = models.DecimalField(db_column='Base_3_DK', max_digits=12, decimal_places=2, blank=True, null=True)
    base_4_dk = models.DecimalField(db_column='Base_4_DK', max_digits=12, decimal_places=2, blank=True, null=True)
    fd_projection = models.DecimalField(db_column='FD_Projection', max_digits=12, decimal_places=2, blank=True, null=True)
    dk_projection = models.DecimalField(db_column='DK_Projection', max_digits=12, decimal_places=2, blank=True, null=True)
    fd_value = models.DecimalField(db_column='FD_Value', max_digits=12, decimal_places=2, blank=True, null=True)
    dk_value = models.DecimalField(db_column='DK_Value', max_digits=12, decimal_places=2, blank=True, null=True)
    batting_order = models.CharField(db_column='Batting_Order', max_length=5, blank=True, null=True)
    id_2 = models.CharField(db_column='ID_2', max_length=12, blank=True, null=True)
    id_3 = models.CharField(db_column='ID_3', max_length=12, blank=True, null=True)
    id_4 = models.CharField(db_column='ID_4', max_length=12, blank=True, null=True)
    id_5 = models.CharField(db_column='ID_5', max_length=12, blank=True, null=True)
    id_6 = models.CharField(db_column='ID_6', max_length=12, blank=True, null=True)
    dk_id_2 = models.CharField(db_column='DK_ID_2', max_length=12, blank=True, null=True)
    dk_id_3 = models.CharField(db_column='DK_ID_3', max_length=12, blank=True, null=True)
    dk_id_4 = models.CharField(db_column='DK_ID_4', max_length=12, blank=True, null=True)
    dk_id_5 = models.CharField(db_column='DK_ID_5', max_length=12, blank=True, null=True)
    dk_id_6 = models.CharField(db_column='DK_ID_6', max_length=12, blank=True, null=True)
    opposing_pitcher = models.CharField(db_column='OpposingPitcher', max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'daily_topflight'

    def __str__(self):
        return self.id
 