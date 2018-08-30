from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import csv
from . import config as config_py

author = "Jeffrey Yang, Allegra Martino, and Daniel Wang"

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

        # Uncomment the below line to get test cases for when the price cap <
        # cost
        # f = open("LeepsCRP/draws/DrawsTest.csv")
        drawsData = list(csv.DictReader(f))

        players_per_group = Constants.players_per_group

        for p in self.get_players():
            p.money = Constants.config[0][self.round_number - 1]["end"]
            p.cost = int(drawsData[players_per_group * (self.round_number - 1) +
                                                (p.id_in_group - 1)]["Cost"])
            p.price_15pts = Constants.config[0][self.round_number - 1]["buy15pts"]
            print("cost is:", p.cost)

            p.benefits = Constants.baseBenefits     # Default to 100

            # Initialization of default values
            p.sold = False
            p.profit = 0
            p.showCurrRound = False

            mode = Constants.config[0][self.round_number - 1]["mode"]
            cont = drawsData[players_per_group * (self.round_number - 1) +
                                (p.id_in_group - 1)]["randomInput"]

            # Generates a random int randomTerm, -5 < randomTerm < 5
            randomTerm = int(-5 + 10 * float(cont))

            # Uncomment the below line to get test cases for when the price cap <
            # cost
            # randomTerm = int(-10 + 10 * float(cont))

            # Mode Keys
            #   1: Price Cap with Participation
            #   2: Auction 3 Reference Price 1
            # 	3: Auction 4 Reference Price 2

            """
            if mode == 1:
                p.priceCap = p.cost + randomTerm + 5
                p.refPrice = None
                p.markup = 5
                p.epsilon_val = randomTerm
            """


            if mode == 1:
                markups = Constants.config[0][self.round_number - 1]["variance"]
                p.markup = random.choice(markups)

                p.priceCap = p.cost + randomTerm + p.markup
                p.epsilon_val = randomTerm
                p.refPrice = None

                """
                elif mode == 2:
                    p.priceCap = p.cost + randomTerm + 15
                    p.markup = 15
                    p.epsilon_val = randomTerm
                    p.refPrice = None
                """

            elif mode == 2:
                p.refPrice = p.cost + randomTerm
                p.priceCap = None

            elif mode == 3:
                p.estimatedCost = p.cost + randomTerm
                p.priceCap = None

        f.close()


class Group(BaseGroup):
    # String consisting of all offers made by sellers (that will eventually be
    # converted into a list
    offers = models.StringField(initial="")
    # markup = models.IntegerField
    # numParticipants = models.IntegerField()
    # showCurrRound = models.BooleanField() # indicate whether the current round
                                          # should be shown in the history table
    # price_15pts = models.IntegerField()

class Player(BasePlayer):
    money = models.FloatField()
    score = models.FloatField()
    cost = models.IntegerField()
    estimatedCost = models.IntegerField()
    sold = models.BooleanField()
    offer = models.IntegerField(blank=True)
    profit = models.IntegerField()

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

    # total number of participants in a given round
    numParticipants = models.IntegerField()

    # max accepted offer for a given round
    max_accepted_offer = models.IntegerField()
    min_accepted_score = models.FloatField()

    # indicate whether the current round should be shown in the history table
    showCurrRound = models.BooleanField()

    price_15pts = models.IntegerField()