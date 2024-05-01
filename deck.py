# deck object for blackjack
from random import randint

class Card:
    def __init__(self, num:int, suit:str) -> None:
        self.num = num
        self.suit = suit
    def __repr__(self) -> str:
        if self.num == 1:
            return f'an Ace of {self.suit}'
        if self.num == 8:
            return f'an 8 of {self.suit}'
        if self.num == 11:
            return f'a Jack of {self.suit}'
        if self.num == 12:
            return f'a Queen of {self.suit}'
        if self.num == 13:
            return f'a King of {self.suit}'
        return f'a {self.num} of {self.suit}'
class Deck:
    def __init__(self) -> None:
        self.draw_pile:list[Card] = []
        self.build_deck()
    def build_deck(self):
        for num in range(1,14):
            for suit in ['Clubs', 'Diamonds', 'Hearts', 'Spades']:
                self.draw_pile.append(Card(num, suit))
    def __iter__(self):
        return iter(self.draw_pile)
    def __next__(self):
        return next(iter(self))
    def __len__(self):
        return len(self.draw_pile)
    def pick_random(self):
        # TODO: delete if not needed
        random_card = self.draw_pile[randint(0, len(self))]
        self.draw_pile.remove(random_card)
        return random_card


    
def main():
    deck = Deck()
    for card in deck:
        print(card)
    print(len(deck.draw_pile))
 
if __name__ == "__main__":
    main()