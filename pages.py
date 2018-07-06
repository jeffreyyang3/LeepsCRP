from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from random import *
import random

class intro(Page):
    def before_next_page(self):
        for p in self.group.get_players():
            p.cost = random.randint(10, 100)

            # Initialization of default values
            p.sold = False
            p.profit = 0

            randomTerm = random.randint(-5, 5)
            # Note: For right now, variance value is set to 8!!
            p.priceCap = p.cost + randomTerm + 8


# Auction 1.1: Price Cap with Participation
class Seller1_1(Page):
    form_model = 'player'
    form_fields = ['participate', 'offer']

    def vars_for_template(self):
        pass

    def before_next_page(self):
        player = self.player

        pass


class Buyer1_1(Page):
    pass

    def vars_for_template(self):
        player = self.player

        print("player participates is: ", player.participate)

class Results1_1(Page):
    pass

class seller1(Page):
    form_model = 'player'
    form_fields = ['offer', 'qualityIncrease']

    def is_displayed(self):
        return self.player.buyer == False

    def vars_for_template(self):
        config = Constants.config

        variance = config[0][self.round_number - 1]["variance"]
        priceBase = config[0][self.round_number - 1]["priceBase"]
        qualityBase = config[0][self.round_number - 1]["qualityBase"]
        noise = config[0][self.round_number - 1]["noise"]

        varInt = random.randint(0,3)
        addRandom = random.randint(1,100) # noise being used temporarily
        self.player.unitPrice = random.randint(priceBase - noise, priceBase + noise)
        self.player.priceCap = self.player.unitPrice * variance[varInt] + addRandom
        self.player.unitQuality = qualityBase

        return {
            'unitPrice': self.player.unitPrice,
            'unitQuality': self.player.unitQuality,
            'priceCap': self.player.priceCap,
        }

class seller2(Page):
    def is_displayed(self):
        return self.player.buyer == False

        


class waitForPrices(WaitPage):


    def after_all_players_arrive(self):
        pass



class buyer1(Page):
    form_model = 'player'
    form_fields = ['buyPrice', 'benefitIncrease']
    def is_displayed(self):
        return self.player.buyer 

    def vars_for_template(self):


        return {
            'money': self.player.money,

        }


    


class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [intro, Seller1_1, Buyer1_1, Results1_1, seller1, waitForPrices, buyer1, seller2, ResultsWaitPage,
    Results
]
