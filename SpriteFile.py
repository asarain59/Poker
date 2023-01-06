# A file containing stuff that can be placed in the game window.
# The classes contained in this file is the ImageSprite class, the Card class which inherits from the ImageSprite class,
#   and then the Deck class which implements objects of type Card

from random import randint  # Used for card shuffling
import pygame


##
# A class which creates a general image sprite
#
class ImageSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        """
        Constructs a general image sprite
        :param x: the starting x-coordinate position of the sprite
        :param y: the starting y-coordinate position of the sprite
        :param filename: the name of the file containing the sprite
        """
        super().__init__()
        self.loadImage(x, y, filename)

    def loadImage(self, x, y, filename):
        """
        Loads the image and makes any necessary pixels transparent, if need be.
        :param x: the starting x-coordinate position of the sprite
        :param y: the starting y-coordinate position of the sprite
        :param filename: the name of the file containing the sprite
        """
        try:
            img = pygame.image.load(filename).convert()
            MAGENTA = (255, 0, 255)
            img.set_colorkey(MAGENTA)

            self.image = img
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y - self.rect.height
        except FileNotFoundError:
            exit(filename + " doesn't exist")

    def moveBy(self, dx, dy):
        """
        Moves the sprite a given number of pixels in both the x- and y- direction
        :param dx: the number of pixels the sprite will be moved horizontally
        :param dy: the number of pixels the sprite will be moved vertically
        """
        self.rect.x = self.rect.x + dx
        self.rect.y = self.rect.y + dy


##
# A class that represents a single playing card
#
class Card(ImageSprite):
    _CARD_LENGTH = 97
    _CARD_WIDTH = 75

    def __init__(self, cardType, x=0, y=0, fileName="DECK_export/faceDown.gif"):
        """
        Constructs a Card
        :param cardType: the name/type of the card
        :param x: the initial x-coordinate that the card will start at
        :param y: the initial y-coordinate that the card will start at
        :param fileName: the name of the file containing the image of the particular card
        """
        super().__init__(x, y, fileName)

        self._cardType = cardType
        self._fileName = fileName

    def getCardName(self):
        """
        Gets the name of the current card.
        :return: the type of that card
        """
        return self._cardType

    def getType(self):
        """
        Gets the type of the card (Ace, 2, 3, ... 10, Jack, Queen, King)
        :return: the card's type
        """
        return self._cardType.split()[0]

    def getSuit(self):
        """
        Gets the suit of the card (Clubs, Diamonds, Hearts, Spades)
        :return: the card's suit
        """
        return self._cardType.split()[2].split(".")[0]

    def hideCard(self):
        """
        Hides the card from the user (Moves it off screen from the canvas)
        """
        self.moveBy(-self.rect.x - self._CARD_WIDTH, -self.rect.y - self._CARD_LENGTH)

    def displayCardAtGivenPos(self, x, y):
        """
        Moves the card to a specified position on the canvas.
        :param x: the x-coordinate canvas position to move the card to
        :param y: the y-coordinate canvas position to move the card to
        """
        self.moveBy(x - self.rect.x, y - self.rect.y - self._CARD_LENGTH)


##
# A class which simulates a deck of cards
#
class Deck:
    TYPES = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
    SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]

    def __init__(self, deckMultiple):
        """
        Creates a CardDeck which is made up of a list of different Card objects.
        :param deckMultiple: the number of 52-card decks to add to a single card deck
        """
        self._cardsInDeck = []
        self._cardsOutOfDeck = []
        self._deckMultiple = deckMultiple

        for i in range(self._deckMultiple):
            for aType in self.TYPES:
                for aSuit in self.SUITS:
                    name = aType + " of " + aSuit
                    self._cardsInDeck.append(Card(name, 0, 0, "DECK_export/" + name + ".gif"))

    def shuffle(self):
        """
        Shuffles the deck by randomizing the card elements in the list.
        """
        for i in range(len(self._cardsInDeck)):
            num = randint(i, len(self._cardsInDeck) - 1)
            aCard = self._cardsInDeck.pop(num)
            self._cardsInDeck.insert(0, aCard)

    def getNumOfCardsInDeck(self):
        """
        Gets the number of cards in the deck which haven't been drawn.
        :return: the number of cards left in the deck
        """
        return len(self._cardsInDeck)

    def getDeckMultiple(self):
        """
        Gets the deck multiple (The number of 52-card decks contained in this deck).
        :return: the deck multiple for this card deck
        """
        return self._deckMultiple

    def addAllCardsBackIntoDeck(self):
        """
        Takes all of the cards which have been drawn out of the deck and puts them back into the card deck at the bottom
        """
        self._cardsInDeck = self._cardsOutOfDeck + self._cardsInDeck
        self._cardsOutOfDeck = []

    def addSpecificCardsBackIntoDeck(self, cardList):
        """
        Adds a list of specific cards which have been taken out of the deck and puts them back into the deck at the
        bottom.
        :param cardList: a list of card objects which will be added into the card deck
        """
        for i in range(len(cardList)):
            if not self.__isInDeck(cardList[i], self._cardsOutOfDeck):  # Makes sure that the card belongs to the deck
                cardList[i] = '0'
            else:
                for j in range(len(self._cardsOutOfDeck)):
                    if cardList[i].getType() == self._cardsOutOfDeck[j].getType():
                        self._cardsOutOfDeck.pop(j)
                        break

        # Any elements containing this value were once Card objects which weren't allowed in the main card deck
        while '0' in cardList:
            cardList.remove('0')

        self._cardsInDeck = cardList + self._cardsInDeck  # Cards get added to the bottom of the deck

    def getCardFromDeck(self):
        """
        Draws a single card from the deck.
        :return: the top card which was in the deck
        """
        # You can't get a card from the deck if the deck is empty
        if len(self._cardsInDeck) == 0:
            exit("Error - There are no more cards left in the deck to take")

        topCard = self._cardsInDeck.pop()
        self._cardsOutOfDeck.append(topCard)

        return topCard

    def viewCardAt(self, index):
        """
        Gets a specific card from within the card deck but doesn't take it out of the deck
        :param index: the index position of the card from within the card deck (list)
        :return: the card at a specified position in the card deck
        """
        try:
            return self._cardsInDeck[index]
        except IndexError:
            exit("Index value " + str(index) + " is out of bounds from range 0-" + str(len(self._cardsInDeck) - 1))

    @staticmethod
    def __isInDeck(cardParam, deckOfCards):
        """
        Checks to see if a card with a specific name exists in a deck of cards.
        :param cardParam: the card, whose name is being checked for in a list of other cards
        :param deckOfCards: a list of cards to be checked to see if a specific card name exists in that deck
        :return: whether or not the card is in the card deck
        """
        for card in deckOfCards:
            if cardParam.getType() == card.getType():
                return True

        return False


##
# A button which can be displayed and clicked
#
class Button:

    def __init__(self, color, x, y, width, height, text="", clickable=True):
        """
        Constructs a button with given attributes.
        @param color the color of the button
        @param x the x-coordinate location of the button
        @param y the y-coordinate location of the button
        @param width the width of the button
        @param height the height of the button
        @param text the text to be displayed on the button
        @param clickable whether or not the button is currently clickable
        """
        self._clickable = clickable
        self._nonClickableColor = (30, 30, 30)
        self._color = color
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._text = text

    def drawButton(self, window, fontSize):
        """
        Draws a button and blits the appropriate text onto the button.
        @param window the window in which the button will be displayed
        @param fontSize the size of the text font that will be placed on the button
        """
        # The color of the button rectangle is drawn
        if self.mouseIsOver(pygame.mouse.get_pos()) and self._clickable:
            pygame.draw.rect(window, self.getDifferentColorShade(self._color, 20),
                             (self._x, self._y, self._width, self._height), 0)
        elif not self._clickable:
            pygame.draw.rect(window, self._nonClickableColor, (self._x, self._y, self._width, self._height), 0)
        else:
            pygame.draw.rect(window, self._color, (self._x, self._y, self._width, self._height), 0)

        if self._text != "" and self._clickable:
            font = pygame.font.SysFont("Arial", int(fontSize), True)
            text = font.render(self._text, True, (0, 0, 0))

            window.blit(text, (self._x + (self._width / 2 - text.get_width() / 2),
                               self._y + (self._height / 2 - text.get_height() / 2)))

    def updateText(self, text):
        """
        Updates the text that is displayed on the button.
        :param text: the text that will replace the original button text
        """
        self._text = text

    def mouseIsOver(self, pos):
        """
        Determines whether or not the user's mouse is currently over the button.
        :param pos: the current mouse position to be checked
        :return: whether or not the mouse is over the button
        """
        if self._x < pos[0] < self._x + self._width and self._y < pos[1] < self._y + self._height:
            return True

        return False

    def changeClickability(self, clickable, window, fontSize):
        """
        Changes whether or not a button is currently clickable.
        :param clickable: makes the button clickable if True and not clickable if False
        :param window: the window in which the button will be displayed
        :param fontSize: the size of the font for the text which is part of the button
        """
        if self._clickable == clickable:
            return

        self._clickable = clickable
        self.drawButton(window, fontSize)

    def isClickable(self):
        """
        Determines whether or not a button can currently be clicked.
        :return: whether or not the button is currently clickable
        """
        return self._clickable

    @staticmethod
    def getDifferentColorShade(color, amount):
        """
        Gets a different color shade of a color.
        :param color: the original color
        :param amount: the amount (positive or negative) used to increase/decrease the brightness of the color
        :return: a new brightened/dimmed version of the original color
        """
        newColor = []
        for i in range(3):
            newColor.append(color[i] + int(amount))
            if newColor[i] < 0:
                newColor[i] = 0
            elif newColor[i] > 255:
                newColor[i] = 255

        return newColor[0], newColor[1], newColor[2]


