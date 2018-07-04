from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'LeepsCRP'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    money = models.CurrencyField()
    buyer = models.BooleanField()
    sellPrice = models.CurrencyField()
    buyPrice = models.CurrencyField()
    noise = models.IntegerField()
    quality = models.IntegerField()
    oppCost = models.CurrencyField()

    

