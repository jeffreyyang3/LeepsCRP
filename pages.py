from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from random import *
import random
from operator import itemgetter

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
            player_offer_string = str(player.id_in_group) + "=" + str(player.offer)

            # group.offers += str(player.offer) + " "
            group.offers += player_offer_string + " "


class WaitForOffers(WaitPage):
    def after_all_players_arrive(self):
        group = self.group

        # Convert offer string into a list
        offer_list = group.offers.split(" ")

        # Remove last element of array which is an empty string
        if offer_list[-1] == "":
            del[offer_list[-1]]

        offer_dict = dict(s.split("=") for s in offer_list)

        # List of dictionaries, each dictionary representing a player who made
        # an offer
        final_offers_list = []

        # Create a new dictionary representing key info for each player that
        # made an offer that will later be added to a list
        for id, player_offer in offer_dict.items():
            player_info = {}
            player_info["id"] = int(id)
            player_info["offer"] = float(player_offer)
            final_offers_list.append(player_info)

        # Sort list of dictionaries according to each dictionary's offer in
        # increasing order
        sorted_final_offers_list = sorted(final_offers_list, key=itemgetter("offer"))
        print("Sorted offers list is: ")
        print(sorted_final_offers_list)

        # NOTE: Only top 2 offers are taken(instead of 8) right now for
        # testing purposes
        if len(sorted_final_offers_list) <= 2:
            chosen_offers = sorted_final_offers_list[:]
        else:
            # NOTE: Only top 2 offers are taken (instead of 8) right now for
            # testing purposes
            chosen_offers = sorted_final_offers_list[:2]

        print("Chosen offers are: ")
        print(chosen_offers)

        for player in chosen_offers:
            for p in group.get_players():
                if player["id"] == p.id_in_group:
                    p.sold = True
                    p.profit = p.offer - p.cost
                    p.money = p.money - p.cost + p.offer


class Buyer1_1(Page):
    def vars_for_template(self):
        player = self.player
        group = self.group


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


page_sequence = [intro, Seller1_1, WaitForOffers, Buyer1_1, Results1_1, seller1,
                 waitForPrices, buyer1, seller2, ResultsWaitPage, Results
]
