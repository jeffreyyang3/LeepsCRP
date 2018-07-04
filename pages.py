from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class intro(Page):
    pass

class seller1(Page):
    def is_displayed(self):
        return self.player.buyer


class buyer1(Page):
    def is_displayed(self):
        return self.player.buyer == False
    


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
    ResultsWaitPage,
    Results

]
