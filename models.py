from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import csv
from . import config as config_py

author = "Jeffrey Yang , Allegra Martino, and Daniel Wang"

doc = """
CRP_2018
"""

class Constants(BaseConstants):
    name_in_url = 'LeepsCRP'
    players_per_group = 3
    num_rounds = 1
    config = config_py.export_data()
    num_rounds = len(config[0])
    baseBenefits = 150

    # The buyer will purchase from the num_bidders_chosen bidders with the lowest
    # scores
    num_bidders_chosen = 2


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()
        f = open("LeepsCRP/draws/Draws4.csv") # hardcoded file name for now
        drawsData = list(csv.DictReader(f))

        players_per_group = Constants.players_per_group

        for p in self.get_players():
            p.money = Constants.config[0][self.round_number - 1]["end"]
            p.cost = int(drawsData[players_per_group * (self.round_number - 1) +
                                                (p.id_in_group - 1)]["Cost"])
            print("cost is:", p.cost)

            p.benefits = Constants.baseBenefits     # Default to 100

            # Initialization of default values
            p.sold = False
            p.profit = 0

            mode = Constants.config[0][self.round_number - 1]["mode"]
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
                p.markup = 5
                p.epsilon_val = randomTerm

            elif mode == 2:
                markups = [1, 3, 5, 8, 12, 15]
                p.priceCap = p.cost + random.choice(markups) + randomTerm

            elif mode == 3:
                p.priceCap = p.cost + randomTerm + 15
                p.markup = 15
                p.epsilon_val = randomTerm

            elif mode == 4:
                p.refPrice = p.cost + randomTerm

            elif mode == 5:
                p.estimatedCost = p.cost + randomTerm

        f.close()


class Group(BaseGroup):
    # String consisting of all offers made by sellers (that will eventually be
    # converted into a list
    offers = models.StringField(initial="")
    # markup = models.IntegerField


class Player(BasePlayer):
    money = models.FloatField()
    score = models.FloatField()
    cost = models.IntegerField()
    estimatedCost = models.IntegerField()
    sold = models.BooleanField()
    offer = models.FloatField(blank=True)
    profit = models.FloatField()

    markup = models.IntegerField()
    epsilon_val = models.IntegerField()

    priceCap = models.IntegerField()
    refPrice = models.IntegerField()
    neighbor_avg_offer = models.FloatField()
    participate = models.BooleanField(choices=[[True, "Yes"], [False, "No"]],
                                      widget=widgets.RadioSelectHorizontal())
    benefits = models.IntegerField()
    benefits_purchased = models.IntegerField()
    benefits_choice = models.IntegerField(widget=widgets.RadioSelect)