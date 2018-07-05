from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from random import *
import random

class intro(Page):
    pass

class seller1(Page):
    form_model = 'player'
    form_fields = ['sellPrice', 'qualityIncrease']
    def is_displayed(self):
        return self.player.buyer == False
    def vars_for_template(self):
        variance = Constants.config[0][self.round_number - 1]["variance"]
        priceBase = Constants.config[0][self.round_number - 1]["priceBase"]
        qualityBase = Constants.config[0][self.round_number - 1]["qualityBase"]
        self.player.unitPrice = random.randint(priceBase - variance,priceBase + variance)
        self.player.unitQuality = qualityBase





        return {
            'unitPrice': self.player.unitPrice,
            'unitQuality': self.player.unitQuality

        }

class seller2(Page):
    def is_displayed(self):
        return self.player.buyer == False

        





class buyer1(Page):
    def is_displayed(self):
        return self.player.buyer 

    


class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    intro,
    buyer1,
    seller1,
    seller2,
    ResultsWaitPage,
    Results

]
