# Final Project: Blackjack

import random

# Represents a playing card
class Card(object):
    
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    SUITS = ["S", "C", "D", "H"]

    def __init__(self, rank, suit, faceUp = True):
        self.rank = rank 
        self.suit = suit
        self.isFaceUp = faceUp
    
    def __str__(self):
        if self.isFaceUp:
            rep = self.rank + self.suit
        else:
            rep = "XX"
        return rep
    
    def flip(self):
        self.isFaceUp = not self.isFaceUp

    # Represents the values of a blackjack card
    ACE_VALUE = 1

    @property
    def value(self):
        if self.isFaceUp:
            v = self.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10
        else:
            v = None
        return v
        

# Represents a hand of cards
class Hand(object):
    
    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:
           rep = ""
           for card in self.cards:
               rep += str(card) + "\t"
        else:
            rep = "empty"
        return rep

    def clear(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def give(self, card, otherHand):
        self.cards.remove(card)
        otherHand.add(card)

# Represents a deck of playing cards
class Deck(Hand):
    
    def populate(self):
        for suit in Card.SUITS:
            for rank in Card.RANKS: 
                self.add(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, hands, perHand = 1):
        for rounds in range(perHand):
            for hand in hands:
                if self.cards:
                    topCard = self.cards[0]
                    self.give(topCard, hand)
                else:
                    print("The deck is out of cards!")
    
# Represents A Blackjack Hand
class BJ_Hand(Hand):
    
    def __init__(self, name):
        super(BJ_Hand, self).__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ":\t" + super(BJ_Hand, self).__str__()  
        if self.total:
            rep += "(" + str(self.total) + ")"        
        return rep

    @property     
    def total(self):
        # if a card in the hand has value of None, then total is None
        for card in self.cards:
            if not card.value:
                return None
        
        # add up card values, treat each Ace as 1
        t = 0
        for card in self.cards:
              t += card.value

        # determine if hand contains an Ace
        contains_ace = False
        for card in self.cards:
            if card.value == Card.ACE_VALUE:
                contains_ace = True
                
        # if hand contains Ace and total is low enough, treat Ace as 11
        if contains_ace and t <= 11:
            # add only 10 since we've already added 1 for the Ace
            t += 10   
                
        return t

    def is_busted(self):
        return self.total > 21

# Represents a Blackjack Player
class BJ_Player(BJ_Hand):
    
    def is_hitting(self):
        response = ask_yes_no("\n" + self.name + ", do you want a hit? (Y/N): ")
        return response == "y"

    def bust(self):
        print(self.name, "busts.")
        self.lose()

    def lose(self):
        print(self.name, "loses.")

    def win(self):
        print(self.name, "wins.")

    def push(self):
        print(self.name, "pushes.")

# Represents a Blackjack Dealer        
class BJ_Dealer(BJ_Hand):
    
    def is_hitting(self):
        return self.total < 17

    def bust(self):
        print(self.name, "busts.")

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()

# Represents the Blackjack Game
class BJ_Game(object):
    
    def __init__(self, names):      
        self.players = []
        for name in names:
            player = BJ_Player(name)
            self.players.append(player)

        self.dealer = BJ_Dealer("Dealer")

        self.deck = Deck()
        self.deck.populate()
        self.deck.shuffle()

    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp

    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()
           
    def play(self):
        # deal initial 2 cards to everyone
        self.deck.deal(self.players + [self.dealer], perHand = 2)
        self.dealer.flip_first_card()    # hide dealer's first card
        for player in self.players:
            print(player)
        print(self.dealer)

        # deal additional cards to players
        for player in self.players:
            self.__additional_cards(player)

        self.dealer.flip_first_card()    # reveal dealer's first 

        if not self.still_playing:
            # since all players have busted, just show the dealer's hand
            print(self.dealer)
        else:
            # deal additional cards to dealer
            print(self.dealer)
            self.__additional_cards(self.dealer)

            if self.dealer.is_busted():
                # everyone still playing wins
                for player in self.still_playing:
                    player.win()                    
            else:
                # compare each player still playing to dealer
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()

        # remove everyone's cards
        for player in self.players:
            player.clear()
        self.dealer.clear()
        


# Ask a yes or no question
def ask_yes_no(question):
    
    response = None
    while response not in ("y", "n"):
        response = input(question).lower()
    return response

# Determines the amount of players
def ask_number(question, low, high):
    
    response = None
    while response not in range(low, high):
        response = int(input(question))
    return response

# Plays the Game
def main():
    print("\t\tWelcome to Blackjack!\n")
    
    names = []
    number = ask_number("How many players? (1 - 2): ", low = 1, high = 3)
    for i in range(number):
        name = input("Enter player name: ")
        names.append(name)
    print()
        
    game = BJ_Game(names)

    again = None
    while again != "n":
        game.play()
        again = ask_yes_no("\nDo you want to play again?: ")


main()
input("\n\nPress the enter key to exit.")





