'''main function for python-blackjack'''
from game import Game

def main():
    '''main loop'''
    done = False
    while not done:
        game = Game()
        while not game.check_end():
            game.new_round()
            game.print_user_status()
            game.stake_players()
            print('---')
            game.print_start_of_round()
            print('---')
            game.hit_players()
            print('---')
            game.win_player()
        userin = input('would you like to play again? (y/n): ')
        if userin == 'n':
            done = True

main()
