from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from random import *
import random
from operator import itemgetter

# Note: Much of the code below can be refactored. However, we should
# do that only when we're sure that the functionality for each auction format is
# correct.

class intro(Page):
    def is_displayed(self):
        return self.round_number == 1

'''
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

        print("Mode:", config[0][self.round_number - 1]["mode"])

        # Add purchased benefits to total amount of player's money
        # Player decided to purchase 10 benefits points for 2/4 ECUs
        if player.benefits_choice == 1:
            player.money -= 2
            player.benefits_purchased = 10

        elif player.benefits_choice == 2:
            player.money -= 6
            player.benefits_purchased = 20

        player.benefits += player.benefits_purchased
'''

# Auction 1.1: Price Cap with Participation
class Seller1_1(Page):
    form_model = 'player'
    form_fields = ['participate', 'offer', 'benefits_choice']

    def benefits_choice_choices(self):
        choice_1 = "Purchase 15 additional benefits points for 2 ECUs"
        choice_2 = "Purchase 30 additional benefits points for 6 ECUs"
        choice_3 = "Purchase no additional benefits points"
        choices = [[1, choice_1], [2, choice_2], [0, choice_3]]

        return choices

    def offer_max(self):
        return self.player.priceCap


    def error_message(self, values):
        if not values["participate"]:
            if not values["offer"] == None:
                return "You must participate in the auction to place an offer."


    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        return mode == 1


    def before_next_page(self):
        config = Constants.config
        group = self.group
        player = self.player

        # Determine benefits purchased by player
        player.benefits_purchased = 0

        print("Mode:", config[0][self.round_number - 1]["mode"])

        # Add purchased benefits to total amount of player's money
        # Player decided to purchase 10 benefits points for 2/4 ECUs
        if player.benefits_choice == 1:
            player.money -= 2
            player.benefits_purchased = 15

        elif player.benefits_choice == 2:
            player.money -= 6
            player.benefits_purchased = 30

        player.benefits += player.benefits_purchased

        # Add player's offer to the full string of offers
        if player.participate:
            player_offer_string = str(player.id_in_group) + "=" + str(player.offer)
            group.offers += player_offer_string + " "


    def vars_for_template(self):
        return {"score_formula": "150 + Benefits Purchased - Price Offered"}


class WaitForOffers(WaitPage):
    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        return mode == 1


    def after_all_players_arrive(self):
        num_bidders_chosen = Constants.num_bidders_chosen
        group = self.group

        # Convert offer string into a list
        offer_list = group.offers.split(" ")

        # Remove last element of the list (an empty string)
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
        print("Unsorted offers list is: ", final_offers_list)

        # Calculation/creation of scores list that includes each player's score
        # final_offers_list should be deleted later on, should only have
        # final_scores_list
        final_scores_list = final_offers_list[:]

        for player_dict in final_scores_list:
            currPlayer = group.get_player_by_id(player_dict["id"])
            currPlayer.score = 150 + currPlayer.benefits_purchased - currPlayer.offer
            player_dict["score"] = currPlayer.score

        # Sort list of dictionaries according to each player's score in
        # increasing order
        sorted_final_scores_list = sorted(final_scores_list,
                                          key=itemgetter("score"), reverse=True)
        print("Sorted scores list is: ")
        print(sorted_final_scores_list)

        # NOTE: Only lowest num_bidders_chosen scores are taken (instead of 8)
        # right now for testing purposes
        if len(sorted_final_scores_list) <= num_bidders_chosen:
            chosen_scores = sorted_final_scores_list[:]
        else:
            # NOTE: Only top num_bidders_chosen offers are taken (instead of 8)
            # right now for testing purposes
            chosen_scores = sorted_final_scores_list[:num_bidders_chosen]

        print("Chosen scores are: ")
        print(chosen_scores)

        for player in chosen_scores:
            chosenPlayer = group.get_player_by_id(player["id"])
            chosenPlayer.sold = True
            chosenPlayer.profit = chosenPlayer.offer - chosenPlayer.cost
            chosenPlayer.money = chosenPlayer.money + chosenPlayer.profit


class Buyer1_1(Page):
    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        return mode == 1


class Results1_1(Page):
    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        return mode == 1


# Auction 2: Price Cap 2
class Seller2_2(Page):
    form_model = 'player'
    form_fields = ['participate', 'offer', 'benefits_choice']

    def benefits_choice_choices(self):
        choice_1 = "Purchase 15 additional benefits points for 2 ECUs"
        choice_2 = "Purchase 30 additional benefits points for 6 ECUs"
        choice_3 = "Purchase no additional benefits points"
        choices = [[1, choice_1], [2, choice_2], [0, choice_3]]

        return choices

    def offer_max(self):
        return self.player.priceCap

    def error_message(self, values):
        if not values["participate"]:
            if not values["offer"] == None:
                return "You must participate in the auction to place an offer."


    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        return mode == 3


    def before_next_page(self):
        config = Constants.config
        player = self.player
        group = self.group

        player.benefits_purchased = 0

        print("Mode:", config[0][self.round_number - 1]["mode"])

        # Add purchased benefits to total amount of player's money
        # Player decided to purchase 10 benefits points for 2/4 ECUs
        if player.benefits_choice == 1:
            player.money -= 2
            player.benefits_purchased = 15

        elif player.benefits_choice == 2:
            player.money -= 6
            player.benefits_purchased = 30

        player.benefits += player.benefits_purchased

        # Add player's offer to the full string of offers
        if player.participate:
            player_offer_string = str(player.id_in_group) + "=" + str(
                player.offer)

            group.offers += player_offer_string + " "

    def vars_for_template(self):
        return {"score_formula": "150 + Benefits Purchased - Price Offered"}


class WaitForOffers2_2(WaitPage):
    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        return mode == 3


    def after_all_players_arrive(self):
        num_bidders_chosen = Constants.num_bidders_chosen
        group = self.group

        # Convert offer string into a list
        offer_list = group.offers.split(" ")

        # Remove last element of array which is an empty string
        if offer_list[-1] == "":
            del [offer_list[-1]]

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

        # Make a copy of final_offers_list
        final_scores_list = final_offers_list[:]

        for player_dict in final_scores_list:
            currPlayer = group.get_player_by_id(player_dict["id"])
            currPlayer.score = 150 + currPlayer.benefits_purchased - currPlayer.offer
            player_dict["score"] = currPlayer.score

        # Sort list of dictionaries according to each player's score in
        # increasing order
        sorted_final_scores_list = sorted(final_offers_list,
                                          key=itemgetter("score"), reverse=True)
        print("Sorted scores list is: ")
        print(sorted_final_scores_list)

        # NOTE: Only lowest num_bidders_chosen scores are taken(instead of 8) right now for
        # testing purposes
        if len(sorted_final_scores_list) <= num_bidders_chosen:
            chosen_scores = sorted_final_scores_list[:]
        else:
            chosen_scores = sorted_final_scores_list[:num_bidders_chosen]

        print("Chosen scores are: ")
        print(chosen_scores)

        for player in chosen_scores:
            chosenPlayer = group.get_player_by_id(player["id"])
            chosenPlayer.sold = True
            chosenPlayer.profit = chosenPlayer.offer - chosenPlayer.cost
            chosenPlayer.money = chosenPlayer.money + chosenPlayer.profit


class Buyer2_2(Page):
    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        return mode == 3


class Results2_2(Page):
    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        return mode == 3


# Auction 3: Reference Price 1
class Seller3_1(Page):
    form_model = 'player'
    form_fields = ['participate', 'offer', 'benefits_choice']

    def benefits_choice_choices(self):
        choice_1 = "Purchase 15 additional benefits points for 2 ECUs"
        choice_2 = "Purchase 30 additional benefits points for 6 ECUs"
        choice_3 = "Purchase no additional benefits points"
        choices = [[1, choice_1], [2, choice_2], [0, choice_3]]

        return choices

    def error_message(self, values):
        if not values["participate"]:
            if not values["offer"] == None:
                return "You must participate in the auction to place an offer."


    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        return mode == 4


    def before_next_page(self):
        config = Constants.config
        player = self.player
        group = self.group

        # Determine benefits purchased by player
        player.benefits_purchased = 0

        print("Mode:", config[0][self.round_number - 1]["mode"])

        # Add purchased benefits to total amount of player's money
        # Player decided to purchase 10 benefits points for 2/4 ECUs
        if player.benefits_choice == 1:
            player.money -= 2
            player.benefits_purchased = 15

        elif player.benefits_choice == 2:
            player.money -= 6
            player.benefits_purchased = 30

        player.benefits += player.benefits_purchased

        # Add player's offer to the full string of offers
        if player.participate:
            player.score = 150 + player.benefits_purchased - 50 * (player.offer / player.refPrice) - (player.refPrice)
            player_score_string = str(player.id_in_group) + "=" + str(player.score)

            group.offers += player_score_string + " "
            print("player_score_string is:", player_score_string)


    def vars_for_template(self):
        return {"score_formula": "150 + Benefits Purchased - 50 * " +
                                 "(Price Offered / Reference Price) - Reference Price"}

class WaitForOffers3_1(WaitPage):
    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        return mode == 4


    def after_all_players_arrive(self):
        num_bidders_chosen = Constants.num_bidders_chosen
        group = self.group

        # Convert offer string into a list
        score_list = group.offers.split(" ")

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
            final_scores_list.append(player_info)

        # Sort list of dictionaries according to each dictionary's offer in
        # increasing order
        sorted_final_scores_list = sorted(final_scores_list,
                                          key=itemgetter("score"), reverse=True)
        print("Sorted scores list is: ")
        print(sorted_final_scores_list)

        # NOTE: Only lowest num_bidders_chosen scores are taken (instead of 8)
        # right now for testing purposes
        if len(sorted_final_scores_list) <= num_bidders_chosen:
            chosen_scores = sorted_final_scores_list[:]
        else:
            chosen_scores = sorted_final_scores_list[:num_bidders_chosen]

        print("Chosen scores are: ")
        print(chosen_scores)

        for player in chosen_scores:
            chosenPlayer = group.get_player_by_id(player["id"])
            chosenPlayer.sold = True
            chosenPlayer.profit = chosenPlayer.offer - chosenPlayer.cost
            chosenPlayer.money = chosenPlayer.money + chosenPlayer.profit


class Buyer3_1(Page):
    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        return mode == 4


class Results3_1(Page):
    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        return mode == 4


class Seller4_2(Page):
    form_model = 'player'
    form_fields = ['participate', 'offer', 'benefits_choice']

    def benefits_choice_choices(self):
        choice_1 = "Purchase 15 additional benefits points for 2 ECUs"
        choice_2 = "Purchase 30 additional benefits points for 6 ECUs"
        choice_3 = "Purchase no additional benefits points"
        choices = [[1, choice_1], [2, choice_2], [0, choice_3]]

        return choices


    def error_message(self, values):
        if not values["participate"]:
            if not values["offer"] == None:
                return "You must participate in the auction to place an offer."


    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        return mode == 5


    def before_next_page(self):
        config = Constants.config
        player = self.player
        group = self.group

        # Determine benefits purchased from player
        player.benefits_purchased = 0

        print("Mode:", config[0][self.round_number - 1]["mode"])

        # Add purchased benefits to total amount of player's money
        # Player decided to purchase 10 benefits points for 2/4 ECUs
        if player.benefits_choice == 1:
            player.money -= 2
            player.benefits_purchased = 15

        elif player.benefits_choice == 2:
            player.money -= 6
            player.benefits_purchased = 30

        player.benefits += player.benefits_purchased

        # Add player's offer to the full string of offers
        if player.participate:
            print("Player", player.id_in_group, "participating")
            player_offer_string = str(player.id_in_group) + "=" + str(
                player.offer)

            print("player_offer_string for player", player.id_in_group, "is", player_offer_string)

            group.offers += (player_offer_string + " ")


    def vars_for_template(self):
        return {"score_formula": "150 + Benefits Purchased - 50 * " +
                                 "(Price Offered / Reference Price) - Reference Price"}

class WaitForOffers4_2(WaitPage):
    def is_displayed(self):
        config = Constants.config
        mode = config[0][self.round_number - 1]["mode"]

        return mode == 5


    def after_all_players_arrive(self):
        num_bidders_chosen = Constants.num_bidders_chosen
        group = self.group

        # Convert offer string into a list
        offer_list = group.offers.split(" ")
        print('group.offers is:', group.offers)
        print("offer list is:", offer_list)

        # Remove last element of array which is an empty string
        if offer_list[-1] == "":
            del [offer_list[-1]]

        # In the dictionary, the player's ID is the key and the offer is the
        # value
        offer_dict = dict(s.split("=") for s in offer_list)
        print("offer_dict is:" + str(offer_dict))

        # List of dictionaries, each dictionary representing a player who made
        # an offer
        final_offers_list = []

        # Create a new dictionary representing key info for each player that
        # made an offer that will later be added to a list
        for id, player_offer in offer_dict.items():
            player_info = {}
            player_info["id"] = int(id)
            player_info["offer"] = float(player_offer)

            currentPlayer = group.get_player_by_id(id)
            player_info["est_cost"] = currentPlayer.estimatedCost

            final_offers_list.append(player_info)

        # Sort list of dictionaries according to each dictionary's offer in
        # increasing order
        print('final offers list is: ')
        print(final_offers_list)

        sorted_final_offers_list = sorted(final_offers_list,
                                          key=itemgetter("est_cost"))

        print("Sorted offers list is: ")
        print(sorted_final_offers_list)

        # Next task: figure out the assignment of the avg_neighbor_offer for
        # each player

        # NOTE: For testing purposes, neighbor's average offer will be the
        # average offer of the *2* participating bidders that are closest to you
        # in terms of estimated costs

        # How many neighbors's offers will be used to calc. average
        max_neighbor_cnt = 2
        # neighbors_counted = 0

        for i in range(len(sorted_final_offers_list)):
            neighbor_avg = 0
            neighbors_counted = 0

            player_dict = sorted_final_offers_list[i]
            player_id = player_dict["id"]
            currentPlayer = group.get_player_by_id(player_id)

            # Case 1: First element in the list
            if i == 0:
                # Take the next 2 elements
                neighbors = sorted_final_offers_list[1: 1 + max_neighbor_cnt]

                for neighbor_dict in neighbors:
                    neighbor = group.get_player_by_id(neighbor_dict["id"])
                    neighbor_avg += neighbor.offer

                neighbor_avg /= max_neighbor_cnt

            # Case 2: Last element in the list
            elif i == len(sorted_final_offers_list) - 1:
                # Take the 3rd to last and 2nd to last elements
                neighbors = sorted_final_offers_list[
                            (-1 * max_neighbor_cnt - 1): -1]

                for neighbor_dict in neighbors:
                    neighbor = group.get_player_by_id(neighbor_dict["id"])
                    neighbor_avg += neighbor.offer

                neighbor_avg /= max_neighbor_cnt

            else:
                left_neigh_index = i - 1
                right_neigh_index = i + 1

                while neighbors_counted < max_neighbor_cnt:
                    # Check for when adding or subtracting to index, left_index
                    # or right_index is out of bounds. This means the remainder of
                    # the opposite end of the list should be taken into account

                    print("left_neigh_index is:", left_neigh_index)
                    print("right_neigh_index is:", right_neigh_index)

                    if left_neigh_index < 0:
                        remaining_neighbors = sorted_final_offers_list[right_neigh_index : (max_neighbor_cnt - neighbors_counted) + i + 1]

                        for p in remaining_neighbors:
                            next_neigh = group.get_player_by_id(p["id"])
                            neighbor_avg += next_neigh.offer
                            neighbors_counted += 1

                        break

                    if right_neigh_index >= len(sorted_final_offers_list):
                        remaining_neighbors = sorted_final_offers_list[left_neigh_index - (max_neighbor_cnt - neighbors_counted) + 1: (left_neigh_index + 1)]

                        for p in remaining_neighbors:
                            next_neigh = group.get_player_by_id(p["id"])
                            neighbor_avg += next_neigh.offer
                            neighbors_counted += 1

                        break

                    left_neighbor = group.get_player_by_id(sorted_final_offers_list[left_neigh_index]["id"])
                    right_neighbor = group.get_player_by_id(sorted_final_offers_list[right_neigh_index]["id"])

                    # Difference in est_cost between current player being looked
                    # at and his/her left neighbor in the list
                    left_neigh_diff = abs(currentPlayer.estimatedCost - left_neighbor.estimatedCost)
                    right_neigh_diff = abs(currentPlayer.estimatedCost - right_neighbor.estimatedCost)

                    print("Left diff is:", left_neigh_diff)
                    print("Right diff is:", right_neigh_diff)

                    # Left neighbor has a closer estimated cost than the right
                    # neighbor
                    if left_neigh_diff <= right_neigh_diff:
                        neighbor_avg += left_neighbor.offer
                        left_neigh_index -= 1

                    # Right neighbor has a closer estimated cost than the left
                    # neighbor
                    else:
                        neighbor_avg += right_neighbor.offer
                        right_neigh_index += 1

                    neighbors_counted += 1

                neighbor_avg /= max_neighbor_cnt

            currentPlayer.refPrice = neighbor_avg
            currentPlayer.neighbor_avg_offer = neighbor_avg

            print("Player in pos", i, "in list has avg", neighbor_avg)

        # Set the scores for each player in the group
        for s in sorted_final_offers_list:
            temp = group.get_player_by_id(s["id"])
            temp.score = 150 + temp.benefits_purchased - 50 * (temp.offer / temp.refPrice) - (temp.refPrice)
            s["score"] = temp.score

        sorted_scores_list = sorted(sorted_final_offers_list,
                                    key=itemgetter("score"), reverse=True)

        print("sorted final scores list:", sorted_scores_list)

        # NOTE: Will only pick num_bidders_chosen lowest scores (for now) for testing purposes

        if len(sorted_scores_list) <= num_bidders_chosen:
            chosen_scores = sorted_scores_list[:]
        else:
            chosen_scores = sorted_scores_list[:num_bidders_chosen]

        print('chosen_scores is:', chosen_scores)

        for player in chosen_scores:
            chosenPlayer = group.get_player_by_id(player["id"])
            chosenPlayer.sold = True
            chosenPlayer.profit = chosenPlayer.offer - chosenPlayer.cost
            chosenPlayer.money = chosenPlayer.money + chosenPlayer.profit


class Buyer4_2(Page):
    def is_displayed(self):
        config = Constants.config
        player = self.player
        mode = config[0][self.round_number - 1]["mode"]

        return mode == 5


class Results4_2(Page):
    def is_displayed(self):
        config = Constants.config
        player = self.player
        mode = config[0][self.round_number - 1]["mode"]

        return mode == 5

page_sequence = [intro,
                 Seller1_1, WaitForOffers, Buyer1_1, Results1_1,
                 Seller2_2, WaitForOffers2_2, Buyer2_2, Results2_2,
                 Seller3_1, WaitForOffers3_1, Buyer3_1, Results3_1,
                 Seller4_2, WaitForOffers4_2, Buyer4_2, Results4_2]