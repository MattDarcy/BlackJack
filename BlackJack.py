'''
BlackJack game in Python
Written by Matthew D'Arcy
'''

from random import randint
from IPython.display import clear_output
import time

decks = []
bet_amt = 0
p_count_card = 0
d_count_card = 0
playagain = True
gameover = False
player = object


# Define Objects: Player, DealersShoe, PlayerHand, DealersHand

class Player(object):
    def __init__(self, name, bankroll):
        self.bankroll = bankroll
        self.name = name
        self.hit = 'y'
        self.playAgain = True

        print
        print 'Good luck, {x}.'.format(x=self.name)
        print

    def add_bankroll(self, amount):
        self.bankroll += amount

    def less_bankroll(self, amount):
        self.bankroll -= amount

class DealersShoe(object):
    def __init__(self, cards):
        self.cards = cards

class PlayerHand(object):
    def __init__(self, c1):
        self.cards = [c1]
        self.total = 0
        self.alt_total = 0
        self.use_hand = 0

class DealersHand(object):
    def __init__(self, c1):
        self.cards = [c1]
        self.total = 0
        self.alt_total = 0
        self.use_hand = 0


# Welcome and user input for name and bankroll

def welcome():
    global player

    print
    print "Welcome to Black-Snake!"
    print

    p_name = raw_input("Please enter your name: ")
    p_bankroll = int(raw_input("Please state how much money you will play with: $"))
    player = Player(p_name, p_bankroll)


# Populate dealer's shoe with the amount of decks the user inputs

def populate_dealers_shoe():
    global decks

    i = 0
    cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    suits = ['h', 's', 'c', 'd']
    deck_qty = int(raw_input("How many decks would you like to play with? "))

    while i < deck_qty:
        for card in cards:
            for _ in suits:
                add_card = str(card)
                decks.append(add_card)
        i += 1

    return decks


# Take user input for the upcoming hand's bet amount

def bet():
    global bet_amt

    bet_amt = player.bankroll + 1

    while bet_amt > player.bankroll or bet_amt < 0:
        bet_amt = int(raw_input("Your bankroll is: ${x} Place your bet: $".format(x=player.bankroll)))
        print
        if bet_amt > player.bankroll:
            print "You don't have that much money."
        if bet_amt < 0:
            print "You cannot bet you will lose, {x}".format(x=player.name)

    time.sleep(1)
    print "Dealing..."
    time.sleep(1)
    

# Draw a card from the dealer's shoe

def draw_card():
    rand = randint(0, len(shoe.cards) - 1)
    card = shoe.cards[rand]
    shoe.cards.remove(shoe.cards[rand])
    return card


# Deal the initial cards to the dealer and the player

def deal():
    global player_hand
    global dealer_hand

    player_hand = PlayerHand(draw_card())
    player_hand.cards.append(draw_card())
    dealer_hand = DealersHand(draw_card())
    dealer_hand.cards.append(draw_card())


# Alter the player's bankroll depending on the outcome of the hand

def transaction():
    print
    
    # Player gets first bust liability

    if player_hand.total > 21 and player_hand.total > 21:
        print 'Player Bust at {x}'.format(x=player_hand.total)
        print
        player.less_bankroll(bet_amt)
        return

    # Then if player didn't bust, check for dealer bust

    if dealer_hand.alt_total > 21 and dealer_hand.total > 21:
        print 'Dealer Bust at {x}'.format(x=dealer_hand.total)
        print
        player.add_bankroll(bet_amt)
        return

    # Player gets first chance at black-jack

    if player_hand.alt_total == 21 or player_hand.total == 21:
        print 'Player BlackSnake'
        print
        player.add_bankroll(bet_amt)
        return

    # Dealer gets second chance at black-jack

    if dealer_hand.alt_total == 21 or dealer_hand.total == 21:
        print 'Dealer BlackSnake'
        print
        player.less_bankroll(bet_amt)
        return

    if dealer_hand.use_hand == player_hand.use_hand:
        print 'Push at {x}'.format(x=dealer_hand.use_hand)
    elif dealer_hand.use_hand > player_hand.use_hand:
        print 'Dealer has won at {x}, player lost at {y}'.format(x=dealer_hand.use_hand, y=player_hand.use_hand)
        player.less_bankroll(bet_amt)
    elif dealer_hand.use_hand < player_hand.use_hand:
        print 'Player has won at {x}, dealer lost at {y}'.format(x=player_hand.use_hand, y=dealer_hand.use_hand)
        player.add_bankroll(bet_amt)


# Check for gameover conditions

def check_game_over():
    global gameover

    # Player gets first bust liability

    if player_hand.total > 21 and player_hand.total > 21:
        gameover = True
        player.hit = 'n'

    # Then if player didn't bust, check for dealer bust

    if dealer_hand.alt_total > 21 and dealer_hand.total > 21:
        gameover = True
        player.hit = 'n'

    # Player gets first chance at black-snake

    if player_hand.alt_total == 21 or player_hand.total == 21:
        gameover = True
        player.hit = 'n'

    # Dealer gets second chance at black-snake

    if dealer_hand.alt_total == 21 or dealer_hand.total == 21:
        gameover = True
        player.hit = 'n'

    # Once player is finished hitting

    if player.hit == 'n':
        player_hand.use_hand = player_hand.total
        dealer_hand.use_hand = dealer_hand.total

        # If higher alt_total results and is not a bust, use alt_total in scoring

        if dealer_hand.alt_total > dealer_hand.total and dealer_hand.alt_total <= 21:
            dealer_hand.use_hand = dealer_hand.alt_total

        if player_hand.alt_total > player_hand.total and player_hand.alt_total <= 21:
            player_hand.use_hand = player_hand.alt_total

def dealer_should_hit():

    # Dealer stands 17 or up on either total or alt_total (soft stand)

    if gameover == False:
        if dealer_hand.total < 17 and (dealer_hand.alt_total < 17 or dealer_hand.alt_total > 21):
            while dealer_hand.total < 17 and (dealer_hand.alt_total < 17 or dealer_hand.alt_total > 21):
                drawn = draw_card()
                print 'dealer new drawn card is {x}'.format(x=drawn)
                dealer_hand.cards.append(drawn)
                totals()

def totals():
    global p_count_card
    global d_count_card

    while p_count_card < len(player_hand.cards):
        if player_hand.cards[p_count_card] == '11' or player_hand.cards[p_count_card] == '12' or player_hand.cards[
            p_count_card] == '13':

            # Special case for J,Q,K all 10's

            player_hand.total += 10
            player_hand.alt_total += 10
        elif player_hand.cards[p_count_card] == '1':

            # Special case for A's can be 1 or 11

            player_hand.total += 1
            player_hand.alt_total += 11
        else:
            player_hand.total += int(player_hand.cards[p_count_card])
            player_hand.alt_total += int(player_hand.cards[p_count_card])
        p_count_card += 1

    while d_count_card < len(dealer_hand.cards):
        if dealer_hand.cards[d_count_card] == '11' or dealer_hand.cards[d_count_card] == '12' or dealer_hand.cards[
            d_count_card] == '13':

            # Special case for J,Q,K all 10's

            dealer_hand.total += 10
            dealer_hand.alt_total += 10
        elif dealer_hand.cards[d_count_card] == '1':

            # Special case for A's can be 1 or 11

            dealer_hand.total += 1
            dealer_hand.alt_total += 11
        else:
            dealer_hand.total += int(dealer_hand.cards[d_count_card])
            dealer_hand.alt_total += int(dealer_hand.cards[d_count_card])
        d_count_card += 1

    # Uncomment the following to check for the resulting score count after each deal/hit

    #print 'player_hand.alt_total is {x}'.format(x=player_hand.alt_total)
    #print 'player_hand.total is {x}'.format(x=player_hand.total)
    #print 'dealer_hand.alt_total is {x}'.format(x=dealer_hand.alt_total)
    #print 'dealer_hand.total is {x}'.format(x=dealer_hand.total)


# Display the current hands

def current_hands():
    clear_output()
    print
    print 'The current hands are: '
    print "{x}'s Hand:".format(x=player.name)
    for card in player_hand.cards:
        print card
    print
    print "Dealer's Hand:"

    itercards = iter(dealer_hand.cards)
    next(itercards) 

    print '?'
    for card in itercards:
        print card
    print


# If player hits, continue to hit otherwise conduct dealer's hits

def hit():
    global gameover

    while gameover == False:

        while player.hit == 'y':
            current_hands()
            totals()
            check_game_over()
            if player.hit == 'y':
                player.hit = raw_input("Hit? (y/n): ")
            if player.hit == 'n':
                dealer_should_hit()
                gameover = True
            elif player.hit == 'y':
                player_hand.cards.append(draw_card())

    current_hands()
    totals()
    check_game_over()
    transaction()


# When a hand is over, display resulting bankroll and reinitialize for another hand or quit the program

def game_over():
    global p_count_card
    global d_count_card
    global bet_amt
    global gameover

    print "{x}, you had bet ${y} and now your bankroll is ${z}".format(x=player.name, y=bet_amt, z=player.bankroll)
    print

    quitting = raw_input("Would you like to quit? (y/n): ")

    if quitting == 'y':
        print
        raise SystemExit('Thanks for playing!')

    player.hit = 'y'
    gameover = False
    p_count_card = 0
    d_count_card = 0
    bet_amt = 0
    player_hand.use_hand = 0
    dealer_hand.use_hand = 0


# Main routine; player and deck quantity remains the same until quitting the program

welcome()
shoe = DealersShoe(populate_dealers_shoe())
while playagain == True:
    bet()
    deal()
    hit()
    game_over()
