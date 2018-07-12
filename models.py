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
 

        for p in self.get_players():
            p.money = Constants.config[0][self.round_number - 1]["end"]
            p.cost = random.randint(10, 100)
            p.benefits = Constants.baseBenefits     # Default to 100

            # Initialization of default values
            p.sold = False
            p.profit = 0

            # p.score = 0
            mode = Constants.config[0][self.round_number - 1]["mode"]
            randomTerm = random.randint(-5, 5)
            if mode == 4:   # Auction 3: Reference Price 1
                p.refPrice = p.cost + randomTerm
            if mode == 3:
                p.price = p.cost + randomTerm + 15
            if mode == 2:
                variance = [1,3,8,12]
                p.priceCap = p.cost + random.choice(variance) + randomTerm
            if mode == 1:
                p.priceCap = p.cost + randomTerm + 5
            if mode == 5:
                p.estimatedCost = p.cost + randomTerm
                
                

                


                

            
            # Note: For right now, markup is set to 8!!
            

class Group(BaseGroup):
    # String consisting of all offers made by sellers(that will eventually be
    # converted into a list
    offers = models.StringField(initial="")
    

class Player(BasePlayer):
    money = models.FloatField()
    buyer = models.BooleanField()

    score = models.FloatField()

    cost = models.IntegerField()
    estimatedCost = models.IntegerField()
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














