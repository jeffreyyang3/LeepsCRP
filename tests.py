from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission
from random import randint, seed, choice


class PlayerBot(Bot):
    def play_round(self):
        group = self.group
        player = self.player
        mode = Constants.config[0][self.round_number - 1]["mode"]

        if self.round_number == 1:
            yield (pages.intro)

        # 2/3 chance that the user participates in the auction
        participate_choice = choice([True, True, False])
        benefits_choice = randint(1, 3)

        if mode == 1:
            if participate_choice:
                if player.priceCap < player.cost or player.priceCap == player.cost:
                    yield Submission(pages.Seller1_1, {'participate': participate_choice, 'offer': player.priceCap, 'benefits_choice': benefits_choice})

                else:
                    offer_choice = randint(player.cost, player.priceCap)
                    yield Submission(pages.Seller1_1, {'participate': participate_choice, 'offer': offer_choice, 'benefits_choice': benefits_choice})
            else:
                yield Submission(pages.Seller1_1, {'participate': participate_choice, 'benefits_choice': benefits_choice})

            yield (pages.Buyer1_1)

        elif mode == 2:
            if participate_choice:
                offer_choice = randint(player.cost, player.cost + 50)
                yield Submission(pages.Seller3_1, {'participate': participate_choice, 'offer': offer_choice, 'benefits_choice': benefits_choice})

            else:
                yield Submission(pages.Seller3_1, {'participate': participate_choice, 'benefits_choice': benefits_choice})

            yield (pages.Buyer3_1)

        else:
            if participate_choice:
                offer_choice = randint(player.cost, player.cost + 50)
                yield Submission(pages.Seller4_2, {'participate': participate_choice, 'offer': offer_choice, 'benefits_choice': benefits_choice})

            else:
                yield Submission(pages.Seller4_2, {'participate': participate_choice, 'benefits_choice': benefits_choice})

            yield (pages.Buyer4_2)