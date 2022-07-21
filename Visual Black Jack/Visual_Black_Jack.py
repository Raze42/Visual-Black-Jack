from multiprocessing.reduction import duplicate
import random, time
from graphics import *

def pick_card():
    suit = "blank"
    value = "blank"
    set = [(random.randint (1,4)), (random.randint(1,13))]
    if (set[0] == 1) :
        suit = "♦"
    if (set[0] == 2) :
        suit = "♣"
    if (set[0] == 3) :
        suit = "♥"
    if (set[0] == 4) :
        suit = "♠"
    if (set[1] <= 10):
        value = str(set[1])
    if (set[1] == 1):
        value = "A"
    if (set[1] == 11):
        value = "J"
    if (set[1] == 12):
        value = "Q"
    if (set[1] == 13):
        value = "K"
    return value+suit

def add_cards(card):
    total = 0
    ace = "no"
    cardval = [x[:-1] for x in card]
    for i in cardval:
        if (i == "A"):
            total = total + 1
            ace = "yes"
        elif (i == "J" or i == "Q" or i == "K"):
            total = total + 10
        elif (i == "B"):
            total = total + 0
        else:
            total = total + int(i)
    if ace == "yes" and total < 12:
        total = total + 10
    return total

def dupl(cards, newcard):
    duplicate = "false"
    count = 0
    for i in cards:
        count = count + 1
        print("comparing card #", count, i, newcard)
        if i == newcard:
            print("Found duplicate: ", i, newcard)
            duplicate == "true"
            return duplicate
    return duplicate

def main():
    debug = "yes"
    if debug == "yes":
        print("debug")

    #create window
    win = GraphWin("Basic Black Jack", 500, 500)
    win.setBackground(color_rgb(255,255,255))
    
    play = "yes"
    while play == "yes" or play == "y":
        player_bust = "no"
        user_message = Text(Point(125,300), "")
        user_message.draw(win)
        result_message = Text(Point(125,335), "")
        result_message.draw(win)

        #initial player cards
        player_cards = [pick_card(), pick_card()]
        while player_cards[0] == player_cards[1]:
            player_cards[1] = pick_card()
        player_cards_str = str(player_cards)
        player_cards_show = Text(Point(125,100), "Player's cards are:\n" + player_cards_str)
        player_cards_show.draw(win)
        #total player cards
        player_cards_total_str = str(add_cards(player_cards))
        player_cards_total = Text(Point(125,135), "Player's cards total: " + player_cards_total_str)
        player_cards_total.draw(win)
        #initial dealer cards
        dealer_cards = [pick_card(), pick_card()]
        while any(item in player_cards for item in dealer_cards):
            print("dealer duplicate found", dealer_cards)
            dealer_cards = [pick_card(), pick_card()]
            print("dealer new cards", dealer_cards)
        dealer_cards_str = str(dealer_cards[0])
        dealer_cards_show = Text(Point(125,200), "Dealer's cards are:\n" + dealer_cards_str)
        dealer_cards_show.draw(win)
        #total dealer cards
        dealer_cards_total_str = str(add_cards(dealer_cards))
        dealer_cards_total = Text(Point(125,235), "Dealer's cards total: " + dealer_cards_total_str)
        dealer_cards_total.draw(win)
        #check for blackjacks
        if (add_cards(dealer_cards) == 21):
            if (add_cards(player_cards) == 21):
                result_message.setText("You and the dealer both have Black Jack! Push!")
            else:
                result_message.setText("Dealer has Black Jack! You lose!")
        elif (add_cards(player_cards) == 21):
            result_message.setText("You have Black Jack! You win!")
        else: #No initial black-jack so begin asking for action
            draws = 2
            result_message.setText("Hit (h) or Stand (s)?")
            action = win.getKey()
            while action == "h" or action == "H":
                draws = draws + 1
                player_cards.insert(draws-1, pick_card())
                #player_cards.append(pick_card())
                while player_cards[draws-1] in player_cards[0:draws-2]:
                    print("player draw duplicate", player_cards[draws-1])
                    player_cards[draws-1] = pick_card()
                    print("replaced with", player_cards[draws-1])
                player_cards_str = str(player_cards)
                player_cards_show.setText("Player's cards are:\n" + player_cards_str)
                player_cards_total_str = str(add_cards(player_cards))
                player_cards_total.setText("Player's cards total: " + player_cards_total_str)
                if add_cards(player_cards) > 21:
                    result_message.setText("Player busts! Dealer Wins.")
                    player_bust = "yes"
                    break
                action = win.getKey()
            if player_bust == "no": #dealer actions
                user_message.setText("Revealing dealer cards...")
                dealer_cards_str = str(dealer_cards)
                dealer_cards_show.setText("Dealer's cards are:\n" + dealer_cards_str)
                dealer_cards_total_str = str(add_cards(dealer_cards))
                dealer_cards_total.setText("Dealer's cards total: " + dealer_cards_total_str)
                draws = 2
                while (add_cards(dealer_cards) < 16):
                    dealer_cards.append(pick_card())
                    draws = draws + 1
                    while dealer_cards[draws-1] in dealer_cards[0:draws-2]:
                        print("dealer draw duplicate", dealer_cards[draws-1])
                        dealer_cards[draws-1] = pick_card()
                        print("replaced with", dealer_cards[draws-1], "at", draws)
                    dealer_cards_str = str(dealer_cards)
                    dealer_cards_show.setText("Dealer's cards are:\n" + dealer_cards_str)
                    dealer_cards_total_str = str(add_cards(dealer_cards))
                    dealer_cards_total.setText("Dealer's cards total: " + dealer_cards_total_str)
                if add_cards(dealer_cards) > 21:
                    result_message.setText("Dealer busts. Player wins.")
                elif add_cards(dealer_cards) == add_cards(player_cards):
                    result_message.setText("Push!")
                elif add_cards(dealer_cards) > add_cards(player_cards):
                    result_message.setText("Dealer Wins")
                elif add_cards(dealer_cards) < add_cards(player_cards):
                    result_message.setText("Player Wins")
        user_message.setText("Would you like to play again?")
        play = win.getKey()
        #clear screen
        player_cards_show.setText("")
        player_cards_total.setText("")
        dealer_cards_show.setText("")
        dealer_cards_total.setText("")
        user_message.setText("")
        result_message.setText("")
    user_message.setText("Click to close.")
    win.getMouse()
    win.close()


main()