from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'LeepsCRP'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()
        numBuyers = 0
        for i in self.get_players():
            print(numBuyers)

            if(numBuyers < 1):
                numBuyers += 1
                i.buyer = True
            else: 
                i.buyer = False 

            






    
            
            
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
    selling = models.BooleanField()



    

