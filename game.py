'''game object for python-blackjack'''
from time import sleep
from deck import Deck
from players import Player, Opponent

class Game:
    '''track and act on game state for python-blackjack'''
    def __init__(self) -> None:
        self.make_players()
        self.deck = Deck()
        self.going = True
        self.dealer = self.players[0]
        self.user = self.players[0]
        self.opponent = self.players[1]
    def __iter__(self):
        return iter(self.players)
    def __next__(self):
        return next(iter(self))
    def __bool__(self):
        return self.going
    def __len__(self):
        return len(self.players)
    def make_players(self):
        '''make player objects'''
        self.players = [Player()]
        self.players.append(Opponent())
    def calculate_pot(self) -> int:
        '''calculate the pot from all player's staked coins'''
        pot = 0
        for player in self:
            pot+= player.bet
        return pot
    def stake_players(self):
        '''call stake_chips method for all players'''
        if self.dealer.name == 'player_1':
            self.opponent.stake_chips(self.user.chips)
            print(f'Player 2 bet {self.opponent.bet} chips', end='. ')
            self.user.bet = self.opponent.bet
        else:
            self.user.stake_chips(self.opponent.chips)
            self.opponent.bet = self.user.bet
        print(f'The pot now has {self.calculate_pot()} chips')
    def hit_players(self):
        '''draw cards for all players'''
        for player in self:
            while player.hit():
                player.draw_card(self.deck)
                if player.name == 'player_1':
                    player.print_count_diff()
                    print('...')
    def new_round(self):
        '''start a new round'''
        print('-----------------------------------------------------------------------------------')
        self.deck = Deck()
        for player in self:
            player.hand = []
            player.draw_card(self.deck)
            player.draw_card(self.deck)
        self.assign_dealer()
    def print_start_of_round(self):
        '''prints start of round data for user'''
        opponent_card = self.opponent.hand[0]
        print(f'your opponent\'s first card is {opponent_card} (known {self.opponent.print_count()})')
        sleep(1)
        print('hand:', self.user.hand, end= ', ')
        print(self.user.print_count())
    def win_player(self):
        '''choose players to have win/lose condition'''
        if self.opponent.check_bust():
            print('the opponent busted')
        if self.user.check_count() == self.opponent.check_count():
            if self.user.check_bust():
                print('both players busted')
            elif self.user.check_blackjack():
                print('both players have a blackjack')
            else:
                print(f'both players have a count of {self.opponent.check_count()}')
            print('tie. Dividing the pot...')
        elif self.user.check_count() == 'blackjack':
            self.opponent.print_count_diff()
            self.user.win()
            self.opponent.lose()
        elif self.opponent.check_count() == 'blackjack':
            self.user.lose()
            self.opponent.win()
        elif self.user.check_count() == 21:
            self.opponent.print_count_diff()
            self.user.win()
            self.opponent.lose()
        elif self.opponent.check_count() == 21:
            print('the opponent has a count of 21')
            self.user.lose()
            self.opponent.win()
        elif self.user.check_bust():
            self.opponent.print_count_diff()
            self.user.lose()
            self.opponent.win()
        elif self.opponent.check_bust():
            self.user.win()
            self.opponent.lose()
        elif self.user.check_count() > self.opponent.check_count():
            self.opponent.print_count_diff()
            self.user.win()
            self.opponent.lose()
        else:
            self.opponent.print_count_diff()
            self.user.lose()
            self.opponent.win()
        input('Press enter to continue...')
    def assign_dealer(self):
        '''assign dealer attribute to next player in sequence'''
        for i, player in enumerate(self.players):
            if self.dealer == player:
                try:
                    self.dealer = self.players[i+1]
                except IndexError:
                    self.dealer = self.players[0]
                self.dealer.is_dealer = True
                player.is_dealer = False
                break
    def print_user_status(self):
        '''print user status'''
        if self.dealer.name == 'player_1':
            print('you are the dealer')
        else:
            print('you are a player')
    def check_end(self):
        '''check if game end condition has happened'''
        active_players = len(self)
        for player in self:
            if player.chips <= 0:
                active_players -= 1
        if active_players == 1:
            if self.opponent.chips <= 0:
                print('you win!')
            else:
                print('you lose!')
            return True
        return False

def main():
    '''main loop'''
    game = Game()
    print(game.players)

if __name__ == "__main__":
    main()
