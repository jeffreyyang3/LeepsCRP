from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from . import config as config_py


author = "Jeffrey Yang and Daniel Wang"

doc = """
CRP_2018
"""

class Constants(BaseConstants):
    name_in_url = 'LeepsCRP'
    players_per_group = None
    num_rounds = 1
    config = config_py.export_data()
    num_rounds = len(config[0])
    baseBenefits = 100


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()
        numBuyers = 0

        for i in self.get_players():
            i.money = Constants.config[0][self.round_number - 1]["end"]

            if numBuyers < 1:
                numBuyers += 1
                i.buyer = True
            else:
                i.buyer = False


class Group(BaseGroup):
    # String consisting of all offers made by sellers(that will eventually be
    # converted into a list
    offers = models.StringField(initial="")
    

class Player(BasePlayer):
    money = models.FloatField()
    buyer = models.BooleanField()

    score = models.FloatField()

    cost = models.IntegerField()
    sold = models.BooleanField()
    offer = models.FloatField()
    profit = models.FloatField()

    buyPrice = models.FloatField()

    noise = models.IntegerField()
    priceCap = models.FloatField()
    refPrice = models.IntegerField()

    oppCost = models.FloatField()
    participate = models.BooleanField(choices=[[True, "Yes"], [False, "No"]], widget=widgets.RadioSelectHorizontal())
    unitPrice = models.FloatField()
    unitQuality = models.IntegerField()

    benefits = models.IntegerField()
    benefits_purchased = models.IntegerField()
    benefits_choice = models.IntegerField(widget=widgets.RadioSelect)

    qualityIncrease = models.CharField(choices=['No increase','increase bit', 'increase lot'], widget=widgets.RadioSelectHorizontal())
    benefitIncrease = models.CharField(choices=['No increase','increase bit', 'increase lot'], widget=widgets.RadioSelectHorizontal())














