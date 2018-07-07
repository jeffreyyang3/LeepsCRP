from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission


class PlayerBot(Bot):
    def play_round(self):

        """
        yield (pages.intro)
        yield Submission(pages.Seller1_1, {'participate': True, 'offer': 23}, check_html=False)
        yield Submission(pages.Buyer1_1, {'player.buyPrice': 202, 'player.benefitIncrease': "increase lot"}, check_html=False)
        yield (pages.Results1_1)
        """