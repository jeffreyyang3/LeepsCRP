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
        noise = Constants.config[0][self.round_number - 1]["noise"]
        varInt = random.randint(0,3)
        addRandom = random.randint(1,100) # noise being used temporarily
        self.player.unitPrice = random.randint(priceBase - noise,priceBase + noise)
        self.player.priceCap = self.player.unitPrice * Constants.config[0][self.round_number - 1]["variance"][varInt] + addRandom
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


page_sequence = [
    intro,
    seller1,
    waitForPrices,
    buyer1,
    seller2,
    ResultsWaitPage,
    Results

]
