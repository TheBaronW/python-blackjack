'''main function for python-blackjack'''
from time import sleep
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
            game.print_start_of_round()
            game.hit_players()
            game.win_player()
            sleep(1)
        userin = input('would you like to play again? (y/n): ')
        if userin == 'n':
            done = True

main()
