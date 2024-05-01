from deck import Deck
from players import Player, Opponent
from time import sleep

class Game:
    '''game state class'''
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
        if self.dealer.name == 'player_1':
            self.opponent.stake_chips(self.user.chips)
            print(f'Player 2 bet {self.opponent.bet} chips', end='. ')
            self.user.bet = self.opponent.bet
        else:
            self.user.stake_chips(self.opponent.chips)
            self.opponent.bet = self.user.bet
        print(f'The pot now has {self.calculate_pot()} chips')
    def hit_players(self):
        for player in self:
            while player.hit():
                player.draw_card(self.deck)
                player.print_count_diff()
    def new_round(self):
        '''start a new round'''
        print('-----------------------------------------------------------------------------------------------')
        self.deck = Deck()
        for player in self:
            player.hand = []
            player.draw_card(self.deck)
            player.draw_card(self.deck)
        self.assign_dealer()
    def print_start_of_round(self):
        '''prints start of round data for user'''
        print('hand:', self.user.hand)
        sleep(2)
        print(f'your opponent\'s first card is {str(self.players[1].hand[0])}')
        sleep(2)
        print('starting', end=' ')
        print(self.user.print_count())
    def win_player(self):
        if self.user.check_count() == self.opponent.check_count():
            print(f'the opponent had a count of {self.opponent.get_count()[0]}')
            print('tie. Dividing the pot...')
            sleep(1)
        elif self.user.check_count() in ['blackjack', 21]:
            print(f'the opponent had a count of {self.opponent.get_count()[0]}')
            self.user.win()
            self.opponent.lose()
        elif self.opponent.check_count() == 'blackjack':
            self.user.lose()
            self.opponent.win()
        elif self.opponent.check_count() == 21:
            print('the opponent had a count of 21')
            self.user.lose()
            self.opponent.win()
        elif self.user.check_bust():
            self.user.lose()
            self.opponent.win()
        elif self.opponent.check_bust():
            print(f'the opponent busted')
            self.user.win()
            self.opponent.lose()
        elif self.user.check_count() > self.opponent.check_count():
            print(f'the opponent had a count of {self.opponent.get_count()[0]}')
            self.user.win()
            self.opponent.lose()
        else:
            print(f'the opponent had a count of {self.opponent.get_count()[0]}')
            self.user.lose()
            self.opponent.win()

        
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
    def print_player_status(self):
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