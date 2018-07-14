from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import csv
from . import config as config_py


author = "Jeffrey Yang and Daniel Wang"

doc = """
CRP_2018
"""

class Constants(BaseConstants):
    name_in_url = 'LeepsCRP'
    # players_per_group = None
    players_per_group = 3


    num_rounds = 1
    config = config_py.export_data()
    num_rounds = len(config[0])
    baseBenefits = 100


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()
        f = open("LeepsCRP/draws/Draws4.csv") # hardcoded file name for now
        drawsData = list(csv.DictReader(f))

        players_per_group = Constants.players_per_group

        for p in self.get_players():
            p.money = Constants.config[0][self.round_number - 1]["end"]

            # p.cost = int(drawsData[8 * (self.round_number - 1) + (p.id_in_group - 1)]["Cost"])
            p.cost = int(drawsData[players_per_group * (self.round_number - 1) +
                                                (p.id_in_group - 1)]["Cost"])
            print("cost is:", p.cost)

            p.benefits = Constants.baseBenefits     # Default to 100

            # Initialization of default values
            p.sold = False
            p.profit = 0

            mode = Constants.config[0][self.round_number - 1]["mode"]

            # cont = drawsData[8 * (self.round_number - 1) +
                             # (p.id_in_group - 1)]["randomInput"]
            cont = drawsData[players_per_group * (self.round_number - 1) +
                                (p.id_in_group - 1)]["randomInput"]

            # Generates a random int randomTerm, -5 < randomTerm < 5
            randomTerm = int(-5 + 10 * float(cont))

            # Mode Keys
            #   1: Auction 1 Price Cap 1
            #   2: Auction 1.1 Price Cap with Participation
            # 	3: Auction 2 Price Cap 2
            #   4: Auction 3 Reference Price 1
            # 	5: Auction 4 Reference Price 2

            if mode == 1:
                p.priceCap = p.cost + randomTerm + 5

            elif mode == 2:
                markups = [1, 3, 8, 12]
                p.priceCap = p.cost + random.choice(markups) + randomTerm

            elif mode == 3:
                # p.price = p.cost + randomTerm + 15
                p.priceCap = p.cost + randomTerm + 15

            elif mode == 4:
                p.refPrice = p.cost + randomTerm

            elif mode == 5:
                p.estimatedCost = p.cost + randomTerm

        f.close()


class Group(BaseGroup):
    # String consisting of all offers made by sellers (that will eventually be
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