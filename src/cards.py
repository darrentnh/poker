import random


class Deck:
    def __init__(self):
        self.deck = [(rank, suit) for suit in 'C D H S'.split() for rank in
             [str(n) for n in range(2, 11)] + list('JQKA')]
        random.shuffle(self.deck)

    def draw_card(self):
        new_card = self.deck.pop()
        # print("Card was drawn", new_card, "Cards left:", len(self.deck))
        return new_card

    def burn_card(self):
        burnt_card = self.deck.pop()
        # print("Card was burnt", burnt_card, "Cards left:", len(self.deck))
        return burnt_card


class Player:
    def __init__(self, player_number):
        # Set player attributes
        self.holecards = set()
        self.player_number = player_number
        self.action_required = 1
        self.current_bid = 0

    def move(self, outstanding_bid):
        """Call this function for individual moves of players"""
        while True:
            print("Player {}'s move. Current bid: ${}".format(self.player_number, self.current_bid))
            print("Player {}'s holecards: {}".format(self.player_number, self.holecards))

            # Logic to determine the available actions
            if self.current_bid == outstanding_bid:
                k, c, r = 1, 0, 1
            elif self.current_bid < outstanding_bid:
                k, c, r = 0, 1, 1

            # Gather input from user according to available actions
            chosen_action_ = input("Type 'F' for fold, 'C' for call, 'K' to check, or 'R' to raise.")
            if str.lower(chosen_action_) == "f":
                print("Player", self.player_number, "has folded\n")
                action = "fold"
                return self.player_number, action

            elif c and str.lower(chosen_action_) == "c":
                print("Player {} has called (${} --> ${})\n".format(self.player_number,
                                                                  self.current_bid, outstanding_bid))
                action = "call"
                return self.player_number, action

            elif k and str.lower(chosen_action_) == "k":
                print("Player", self.player_number, "has checked\n")
                action = "check"
                return self.player_number, action

            elif r and str.lower(chosen_action_) == "r":
                action = "raise"
                while True:
                    amount = input("Type the amount you want to raise to.")
                    try:
                        amount = int(amount)
                        if amount <= outstanding_bid:
                            raise AssertionError
                        break
                    except ValueError:
                        print("Please enter an integer")
                    except AssertionError:
                        print("Please enter a higher value")
                print("Player {} has raised (${} --> ${})\n".format(self.player_number,
                                                                    outstanding_bid, amount))
                self.current_bid = amount
                return self.player_number, action, amount

            elif (str.lower(chosen_action_) == "c" or str.lower(chosen_action_) == "k" or
                          str.lower(chosen_action_) == "r"):
                print("You may not do that.\n")

            else:
                print("I did not understand your input.\n")
        # money


class Game:
    def __init__(self, players):
        """Takes an integer number of players"""
        # Setup of deck
        self.deck = Deck()
        self.community_cards = set()
        self.street = ("Preflop", "Flop", "Turn", "River")
        self.outstanding_bid = 2  # Big blind

        # Setup of players
        self.existing_players = {}

        for i in range(players):
            self.existing_players[i+1] = Player(i+1)
        print("Staring a game with {} players".format(len(self.existing_players)))
        for player in self.existing_players.values():
            player.holecards.add(self.deck.draw_card())
            player.holecards.add(self.deck.draw_card())
            print("Player {}'s holecards: {}".format(player.player_number, player.holecards))

        # Set small blind and big blind
        self.existing_players[1].current_bid = 1  # Small Blind
        self.existing_players[2].current_bid = 2  # Big Blind

    def start(self):
        """Core function to play the game iterating through 4 streets after instantiating players"""
        print("Blinds are $1/$2.\nPlayer 1 will start as the small blind.\n")

        # Iterating through the 4 streets
        for street in self.street:
            print("-" * 10, "Current street:", street, "-" * 10)

            while self.check_action_required():
                for player in list(self.existing_players.values()):
                    print("Bid to match: $", self.outstanding_bid)
                    self.check_response(player)
                    self.check_all_folded()
                    if not self.check_action_required():  # to fix odd number of turns e.g. R, R, C
                        break

            print("-" * 12, street, "ends", "-" * 12, "\n")
            self.between_streets(street)

    def between_streets(self, street):
        # Burn and deal community cards
        self.deck.burn_card()
        if street == "Preflop":
            for i in range(3):
                self.community_cards.add(self.deck.draw_card())
        elif street == "River":
            pass
        else:
            self.community_cards.add(self.deck.draw_card())
        print("Community Cards", self.community_cards, "\n")

        # Reset action_required and current bid for next street
        for player in list(self.existing_players.values()):
            player.action_required = 1
            player.current_bid = 0

        # Reset self.outstanding_bid for next street
        self.outstanding_bid = 0

    def check_action_required(self):
        for k, v in list(self.existing_players.items()):
            if self.existing_players[k].action_required == 1:
                return True

    def check_response(self, player):
        other_players = [x for x in self.existing_players.values() if x is not player]
        response = player.move(self.outstanding_bid)
        player.action_required = 0
        if response[1] == "raise":
            self.outstanding_bid = response[2]
            # set all other players action_required = 1.
            for i in range(len(other_players)):
                other_players[i].action_required = 1
        elif response[1] == "call":
            # Update current bid to match outstanding bid
            player.current_bid = self.outstanding_bid
        elif response[1] == "fold":
            player.is_in_game = 0
            self.existing_players.pop(player.player_number)

    def check_all_folded(self):
        # check if everybody else folded
        if len(self.existing_players) == 1:
            last_player = [(k, v) for (k, v) in self.existing_players.items()][0]
            print("Player", last_player[1].player_number, "is the winner!")
            input("Press enter to quit the game.")
            quit()

    def show_down(self):
        pass # TODO: determine hand rank


Game(3).start()
