from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from random import *
import random
from operator import itemgetter

class intro(Page):
    pass


class BuyBenefits(Page):
    form_model = 'player'
    form_fields = ['benefits_choice']

    def benefits_choice_choices(self):
        choice_1 = "Purchase 10 additional benefits points for 2 ECUs"
        choice_2 = "Purchase 20 additional benefits points for 6 ECUs"
        choice_3 = "Purchase no additional benefits points"
        choices = [[1, choice_1], [2, choice_2], [0, choice_3]]

        return choices

    def before_next_page(self):
        config = Constants.config
        player = self.player

        player.benefits_purchased = 0

        # Add purchased benefits to total amount of player's money
        # Player decided to purchase 10 benefits points for 2/4 ECUs
        if player.benefits_choice == 1:
            player.money -= 2
            player.benefits_purchased = 10
            # player.benefits += player.benefits_purchased

        elif player.benefits_choice == 2:
            player.money -= 6
            player.benefits_purchased = 20
            # player.benefits += player.benefits_purchased

        player.benefits += player.benefits_purchased
        # And if player.choice equals 0, the player didn't purchase any
        # additional benefits

        # print("Player's benefits are now:", player.benefits)

  

        


# Auction 1.1: Price Cap with Participation
class Seller1_1(Page):
    form_model = 'player'
    form_fields = ['participate', 'offer']

    def offer_max(self):
        return self.player.priceCap

    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        # print("Auction 1: Price Cap 1")
        return mode == 1

    def before_next_page(self):
        player = self.player
        group = self.group

        # Add player's offer to the full string of offers
        if player.participate:
            player_offer_string = str(player.id_in_group) + "=" + str(player.offer)

            group.offers += player_offer_string + " "


class WaitForOffers(WaitPage):
    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        # print("Auction 1: Price Cap 1, Waiting for Offers")
        return mode == 1

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
    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        # print("Auction 1: Price Cap 1 Buyer Page")
        return mode == 1

    def vars_for_template(self):
        player = self.player
        group = self.group


class Results1_1(Page):
    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        # print("Auction 1: Price Cap 1")

        return mode == 1


# Auction 3: Reference Price 1
class Seller3_1(Page):
    form_model = 'player'
    form_fields = ['participate', 'offer']

    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        # print("Auction 3: Reference Price 1")

        return mode == 4

    def before_next_page(self):
        player = self.player
        group = self.group

        for y in group.get_players():
            print("player score in bef next pg is before setting val is:", y.score)

        # Add player's offer to the full string of offers
        if player.participate:
            player.score = 100 + player.benefits_purchased - 50 * (player.offer / player.refPrice) - player.refPrice

            print("Player's score is:", player.score)

            player_score_string = str(player.id_in_group) + "=" + str(player.score)
            print("player_score_string is:", player_score_string)

            group.offers += player_score_string + " "
            print("Player's score is right before exiting if statement:", player.score)

        for x in group.get_players():
            print("player score in bef next pg is:", x.score)

class WaitForOffers3_1(WaitPage):
    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        # print("Auction 3: Reference Price 1, Waiting for Offers")

        return mode == 4 or mode == 5

    def after_all_players_arrive(self):
        group = self.group
        # Convert offer string into a list
        score_list = group.offers.split(" ")

                             
                
        

        for x in group.get_players():
            print("player score in dict beg is:", x.score)

        

        # Remove last element of array which is an empty string
        if score_list[-1] == "":
            del [score_list[-1]]

        score_dict = dict(s.split("=") for s in score_list)

        # List of dictionaries, each dictionary representing a player who made
        # an offer
        final_scores_list = []

        # Create a new dictionary representing key info for each player that
        # made an offer that will later be added to a list
        for id, player_score in score_dict.items():
            player_info = {}
            player_info["id"] = int(id)
            player_info["score"] = float(player_score)
            print("Inside dictionary, player score is:", player_score)
            final_scores_list.append(player_info)

        # Sort list of dictionaries according to each dictionary's offer in
        # increasing order
        sorted_final_scores_list = sorted(final_scores_list,
                                          key=itemgetter("score"))
        print("Sorted scores list is: ")
        print(sorted_final_scores_list)

        # NOTE: Only lowest 2 scores are taken (instead of 8) right now for
        # testing purposes
        if len(sorted_final_scores_list) <= 2:
            chosen_scores = sorted_final_scores_list[:]
        else:
            # NOTE: Only top 2 offers are taken (instead of 8) right now for
            # testing purposes
            chosen_scores = sorted_final_scores_list[:2]

        print("Chosen scores are: ")
        print(chosen_scores)

        # print("Auction 3: Reference Price 1, Buyer Page")

        for player in chosen_scores:
            for p in group.get_players():
                if player["id"] == p.id_in_group:
                    p.sold = True
                    p.profit = p.offer - p.cost
                    p.money = p.money - p.cost + p.offer

    def vars_for_template(self):
        pass

class Buyer3_1(Page):
    def is_displayed(self):
        config = Constants.config
        player = self.player
        mode = config[0][self.round_number - 1]["mode"]

        # print("Auction 3: Reference Price 1, Buyer Page")

        return mode == 4


class Results3_1(Page):
    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        # print("Auction 3: Reference Price 1, Results Page")

        return mode == 4


#page_sequence = [intro, Seller1_1, WaitForOffers, Buyer1_1, Results1_1, 
 #                waitForPrices, buyer1, seller2, ResultsWaitPage, Results]
page_sequence = [intro, BuyBenefits, Seller1_1, WaitForOffers, Buyer1_1, Results1_1,
                 Seller3_1, WaitForOffers3_1, Buyer3_1, Results3_1]
