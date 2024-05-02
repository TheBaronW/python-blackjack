'''player objects for python-blackjack'''
from random import randint
from abc import ABC, abstractmethod
from deck import Card, Deck

class Person(ABC):
    '''abstract class for actor objects'''
    def __init__(self, name:str):
        self.chips = 10
        self.hand:list[Card] = []
        self.bet:int = 0
        self.name = name
        self.is_dealer = False
    def __repr__(self) -> str:
        return self.name
    @abstractmethod
    def hit(self):
        '''abstract method to be implemented in concrete'''
    @abstractmethod
    def stake_chips(self, dealer_chips):
        '''abstract method to be implemented in concrete'''
    @abstractmethod
    def print_count_diff(self):
        '''prints ui style count for concrete object'''
    def draw_card(self, deck:Deck):
        '''draw Card from Deck object'''
        random_card:Card = deck.pick_random()
        self.hand.append(random_card)
    def check_count(self):
        '''check if count is equal to 21'''
        num = self.get_count()[1]
        point_count = self.get_count()[0]
        if self.check_blackjack():
            return 'blackjack'
        if self.check_bust():
            return 'bust'
        if self.get_count()[0] == 21:
            return 21
        if 21-num < 21-point_count:
            return num
        return point_count
    def check_bust(self):
        '''check if point cound is above 21'''
        point_count = 0
        for card in self.hand:
            if card.num in range(2, 11):
                point_count+=card.num
            elif card.num > 10:
                point_count+= 10
            else:
                point_count+=1
        if point_count > 21:
            return True
        return False
    def print_count(self, hand = None):
        '''print count to terminal'''
        num = self.get_count(hand)[1]
        count = self.get_count(hand)[0]
        aces = self.get_count(hand)[2]
        if aces > 0 and num:
            return f'count: {count} (soft {num})'
        return f'count: {count}'
    def check_blackjack(self):
        '''check if hand has "natural" 21 (ace and ten-card)'''
        if len(self.hand) == 2:
            if 1 in [self.hand[0].num, self.hand[1].num]:
                if self.hand[0].num >= 10 or self.hand[1].num >= 10:
                    return True
        return False
    def win(self):
        '''win condition'''
        self.chips += self.bet
    def lose(self):
        '''lose condition'''
        self.chips -= self.bet

    def get_count(self, hand = None):
        '''return count of self from self.hand values'''
        aces_11 = 0
        point_count = 0
        if hand is None:
            hand = self.hand
        calc_list = []
        for card in hand:
            if card.num >= 2:
                point_count+=card.value
            elif card.num == 1:
                aces_11+=1
        aces_1 = 0
        num = False
        # handles case of ace(s) in hand
        while aces_11 != 0:
            calc_list.append(point_count + aces_1 + (aces_11 * 11))
            calc_list.sort(reverse=True)
            for x in calc_list:
                if x <= 21:
                    num = x
            if point_count + aces_1 + (aces_11 * 11) == 21:
                return [21, num, aces_1+aces_11]
            aces_1+=1
            aces_11-=1
        return [point_count+aces_1, num, aces_1+aces_11]




class Player(Person):
    '''user actor object'''
    def __init__(self, name = "player_1"):
        super().__init__(name)
        self.is_dealer = True
    def print_count_diff(self):
        print(f'you drew {str(self.hand[-1])} and you have {self.print_count()[7:]} points')
    def stake_chips(self, dealer_chips:int):
        ''' if not dealer, prompt user to stake an amount of chips less or equal to dealer chips'''
        print(f'you have {self.chips} chips, and your opponent has {dealer_chips} chips')
        done = False
        if not self.is_dealer:
            while not done:
                amount = input('type the number of chips you\'d like to bet (default 1): ')
                try:
                    amount = int(amount)
                except ValueError:
                    if amount == '':
                        self.bet = 1
                        print('staking 1 chip', end='. ')
                        done = True
                    else:
                        print('invalid input')
                else:
                    if amount > self.chips:
                        print('you can\'t stake more chips than you have')
                    elif amount > dealer_chips:
                        print(f'you can\'t stake more chips than the opponent has ({dealer_chips})')
                    else:
                        print(f'staking {amount} chips', end= '. ')
                        self.bet = amount
                        done = True
            return False
        return True
    def win(self):
        super().win()
        print('you win the pot!')
    def lose(self):
        super().lose()
        print('the opponent wins the pot')

    def hit(self):
        if self.check_count() == 'blackjack':
            print('you got a blackjack!')
            input('Press Enter to continue...')
            return False
        if self.check_bust():
            print('you busted...')
            input('Press enter to continue...')
            return False
        if self.check_count() == 21:
            print('you got a 21')
            input('Press enter to continue...')
            return False
        if self.is_dealer:
            if self.check_count() < 17:
                input('below 17, so you must hit. Enter to continue...')
                return True
            input(f'{self.check_count()} is 17 or above, so you must stand. Enter to continue...')
            return False
        userin = input('would you like to hit? (draw a card y/n): ')
        if userin != 'n':
            return True
        return False

class Opponent(Person):
    '''CPU actor object'''
    def __init__(self, name = "player_2"):
        super().__init__(name)
        self.bet = 1
    def stake_chips(self, dealer_chips:int):
        '''if not dealer, stake a random amount of chips'''
        if not self.is_dealer:
            if dealer_chips < 4:
                self.bet = randint(1, dealer_chips)
            elif self.chips < 4:
                self.bet = randint(1, self.chips)
            else:
                self.bet = randint(1, 4)
    def print_count(self, hand = None):
        return super().print_count([self.hand[0]])
    def print_count_diff(self):
        '''prints ui style count for opponent object'''
        print(f'the opponent has a count of {self.check_count()}')
    def hit(self):
        if self.check_count() == 'blackjack':
            print(f'{self.name} got a blackjack!')
            return False
        if self.check_count() == 'bust':
            return False
        if self.check_count() is True:
            return False
        if self.is_dealer:
            if self.check_count() < 17:
                return True
            return False
        if self.check_count() < 15:
            return True
        return False

def main():
    player = Player()
    player.hand.append(Card(1, 'spades'))
    player.hand.append(Card(1, 'spades'))
    player.hand.append(Card(1, ''))
    player.hand.append(Card(1, ''))
    player.hand.append(Card(1, 'spades'))
    player.check_count()

if __name__ == "__main__":
    main()
