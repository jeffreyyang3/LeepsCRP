from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from . import config as config_py


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'LeepsCRP'
    players_per_group = None
    num_rounds = 1
    config = config_py.export_data()
    num_rounds = len(config[0])


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()
        numBuyers = 0
        for i in self.get_players():

            if(numBuyers < 1):
                numBuyers += 1
                i.buyer = True
            else: 
                i.buyer = False 



class Group(BaseGroup):
    pass
    





class Player(BasePlayer):
    money = models.FloatField()
    buyer = models.BooleanField()
    sellPrice = models.FloatField()
    buyPrice = models.FloatField()
    noise = models.IntegerField()
    oppCost = models.FloatField()
    selling = models.BooleanField()
    unitPrice = models.FloatField()
    unitQuality = models.IntegerField()
    qualityIncrease = models.CharField(choices=['No increase','increase bit', 'increase lot'], widget=widgets.RadioSelectHorizontal())



    

