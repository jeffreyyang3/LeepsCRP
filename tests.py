from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission
from random import randint, seed


class PlayerBot(Bot):
    def play_round(self):
        group = self.group
        player = self.player

        yield (pages.intro)
        yield Submission(pages.BuyBenefits, {'benefits_choice': randint(0, 2)}, check_html=False)
        yield Submission(pages.Seller4_2, {'participate': True, 'offer': randint(10, player.estimatedCost + 30)}, check_html=False)
        yield Submission(pages.Buyer4_2, {}, check_html=False)
        yield (pages.Results4_2)
        