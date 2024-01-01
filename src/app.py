import random

suits = ['clubs', 'diamonds', 'hearts', 'spades']
faces = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


class Card:
    def __init__(self, suit, face):
        self._suit = suit
        self._face = face

    def get_suit(self):
        return self._suit

    def get_face(self):
        return self._face


class Deck:
    deck = []

    def __init__(self, faces_in_deck=faces):
        self.faces_in_deck = faces_in_deck
        self.deck = []
        for face in self.faces_in_deck:
            for suit in suits:
                self.deck.append(Card(suit, face))

    def cut(self):
        shift_position = random.randint(1, len(self.deck) - 1)
        self.deck = self.deck[shift_position:] + self.deck[:shift_position]

    def shuffle(self):
        random.shuffle(self.deck)

    def get_cards(self):
        return self.deck


class Player:
    players_cards = []

    def __init__(self):
        self.players_cards = []

    def get_cards(self):
        return self.players_cards


class Game:
    players = []
    deck = []

    def __init__(self, number_of_players, dealing_direction, 
                dealing_instructions):
        self.number_of_players = number_of_players
        self.dealing_direction = dealing_direction
        self.dealing_instructions = dealing_instructions
        self.deck = Deck()
        self.players = [Player() for _ in range(self.number_of_players)]

    def get_players(self):
        return self.players

    def prepare_deck(self):
        for player in self.players:
            self.deck.deck += player.get_cards()
            player.players_cards = []
        self.deck.shuffle()
        self.deck.cut()

    def deal(self, first_player):
        if self.dealing_direction == 'rtl':
            self.players.reverse()
        index = self.players.index(first_player)
        self.players = self.players[index:] + self.players[:index]

        for instruction in self.dealing_instructions:
            for player in self.players:
                player.players_cards.extend(self.deck.deck[:instruction])
                self.deck.deck = self.deck.deck[instruction:]

    def get_deck(self):
        return self.deck


class Belot(Game):
    def __init__(self):
        Game.__init__(self, 4, 'ltr', (2, 3, 3))
        self.deck = Deck(['7', '8', '9', '10', 'J', 'Q', 'K', 'A'])


class Poker(Game):
    def __init__(self):
        Game.__init__(self, 9, 'rtl', (1, 1, 1, 1, 1))
