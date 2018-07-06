from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from random import *
import random

class intro(Page):
    def before_next_page(self):
        # self.group.offers = ""

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

    def offer_max(self):
        return self.player.priceCap

    def vars_for_template(self):
        pass

    def before_next_page(self):
        player = self.player
        group = self.group

        # Add player's offer to the full string of offers
        if player.participate:
            print("group offers before adding is: ")
            print(group.offers)
            group.offers += str(player.offer) + " "

            print("group offers is now:")
            print(group.offers)

        pass

class WaitForOffers(WaitPage):
    def after_all_players_arrive(self):
        group = self.group

        print("list of all offers is: ")
        print(group.offers)

        # Convert offer string into a list
        offer_list = group.offers.split(" ")

        # Remove space in last space of array
        if offer_list[-1] == "":
            del[offer_list[-1]]

        print("Offer list is: ")
        print(offer_list)

        offer_list.sort()
        print("Sorted offer list is:")
        print(offer_list)

        # NOTE: Only top 2 offers are taken(instead of 8) right now for
        # testing purposes
        if len(offer_list) <= 2:
            chosen_offers = offer_list[:]
        else:
            # NOTE: Only top 2 offers are taken (instead of 8) right now for
            # testing purposes
            chosen_offers = offer_list[:2]

        print("Chosen offers are: ")
        print(chosen_offers)


class Buyer1_1(Page):
    pass

    def vars_for_template(self):
        player = self.player
        group = self.group


        # print("list of all offers is: ")
        # print(group.offers)
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


page_sequence = [intro, Seller1_1, WaitForOffers, Buyer1_1, Results1_1, seller1, waitForPrices, buyer1, seller2, ResultsWaitPage,
    Results
]
