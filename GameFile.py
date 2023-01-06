# File containing the GameBase class and the PokerGame class which inherits from GameBase

from SpriteFile import Card, Deck, Button
import pygame
import time


##
# A GameBase superclass that implements all the functionalities of pygame but makes everything more simplified
#
class GameBase:
    def __init__(self, width, height):
        """
        Constructs a general game base for a window in pygame
        :param width: the width of the window which will display the game
        :param height: the height of the window
        """
        pygame.init()
        self._width = width
        self._height = height

        self._display = pygame.display.set_mode((self._width, self._height))
        self._clock = pygame.time.Clock()
        self._framesPerSecond = 30
        self._sprites = pygame.sprite.LayeredUpdates()
        self._ticks = 0
        pygame.key.set_repeat(1, 120)

    def getDisplay(self):
        """
        Gets the pygame window display.
        :return: the display
        """
        return self._display

    def getClock(self):
        """
        Gets the pygame clock.
        :return: the clock
        """
        return self._clock

    def getTicks(self):
        """
        Gets the pygame ticks.
        :return: the ticks
        """
        return self._ticks

    def getFramesPerSecond(self):
        """
        Gets the number of frames per second being displayed.
        :return: the frames per second
        """
        return self._framesPerSecond

    def getCanvasDimensions(self):
        """
        Gets the width/height dimension of the canvas.
        :return: the canvas dimensions, showing the width and height as a tuple
        """
        dim = self._width, self._height
        return dim

    def mouseButtonDown(self, x, y):
        """
        This function is called whenever the mouse button is clicked
        :param x: the x-coordinate of the mouse
        :param y: the y-coordinate of the mouse
        """
        return

    def keyDown(self, key):
        """
        This function is called whenever a key is pressed
        :param key: the key that was pressed
        """
        return

    def update(self):
        """  Updates the current state of the pygame window  """
        self._sprites.update()

    def draw(self):
        """  Draws the sprites on the canvas  """
        self._sprites.draw(self._display)

    def add(self, sprite):
        """
        Adds a sprite to the group of sprites for the canvas
        :param sprite: the sprite to be added to the group
        """
        self._sprites.add(sprite)

    def updateTicks(self, value):
        """
        Updates the ticks for the pygame window
        :param value: the tick value
        """
        self._ticks += value

    @staticmethod
    def quit():
        """  Exits the pygame window  """
        pygame.quit()

    def run(self):
        """  Runs the pygame window and keeps track of any events from the user  """

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouseButtonDown(event.pos[0], event.pos[1])
                elif event.type == pygame.KEYDOWN:
                    self.keyDown(event.key)

            self.update()
            WHITE = (255, 255, 255)
            self._display.fill(WHITE)
            self.draw()
            pygame.display.update()
            self._clock.tick(self._framesPerSecond)
            self._ticks = self._ticks + 1


##
# A Window that runs a game of Texas Hold 'em
#
class PokerGame(GameBase):
    _CARD_HANDS = ["Royal Flush", "Straight Flush", "Four of a Kind", "Full House", "Flush", "Straight",
                   "Three of a Kind", "Two Pairs", "One Pair", "No Pair"]

    _MINIMUM_BET_WAGE = 20  # In dollars
    _START_BALANCE = 500  # In dollars
    _COMPUTER_WAIT_TIME = 1  # In seconds (The time the user waits for the computer to make a move)
    _TEXT_DATA_LENGTH = 6

    def __init__(self, width, height):
        """
        Constructs the window for the poker game and all of its instance variables
        :param width: the width of the poker game window
        :param height: the height of the poker game window
        """
        super().__init__(width, height)
        self._startTime = -1
        self._textData = [] * self._TEXT_DATA_LENGTH

        self._winner = "No Winner"
        self._userHand = "None"
        self._computerHand = "None"

        self._roundHasEnded = False
        self._userFolded = False
        self._computerHasTurn = False
        self._computerTurnStartTime = 0

        self._userMoney = self._START_BALANCE
        self._computerMoney = self._START_BALANCE

        self._currentPot = 0
        self._currentWager = self._MINIMUM_BET_WAGE
        self._currentBeingRisked = 0

        self._foldButton = Button((215, 1, 49), 20, 20, 80, 50, "Fold")
        self._callButton = Button((254, 159, 49), 110, 20, 80, 50, "Call ($" + str(self._currentWager) + ")")
        self._raiseButton = Button((1, 175, 104), 200, 20, 80, 50, "Raise ($" + str(self._currentWager) + ")")

        self._newRoundButton = Button((181, 223, 81), 130, 20, 100, 50, "Start New Round")
        self._exitGameButton = Button((210, 70, 38), 40, 20, 80, 50, "Exit Game")

        self._cardDeck = Deck(1)
        self._cardDeck.shuffle()

        self._blankCard = [Card("Unknown", 0, 0, "DECK_export/faceDown.gif"),
                           Card("Unknown", 0, 0, "DECK_export/faceDown.gif")]

        super().add(self._blankCard[0])
        super().add(self._blankCard[1])

        self._userCard1 = Card("Empty")
        self._userCard2 = Card("Empty")
        self._computerCard1 = [Card("Empty"), self._blankCard[0]]
        self._computerCard2 = [Card("Empty"), self._blankCard[1]]

        self._displayCards = [Card("Empty"), Card("Empty"), Card("Empty"), Card("Empty"), Card("Empty")]
        self._cardsInDisplay = 0

        # Adds each card sprite to the group of sprites linked to this canvas
        for i in range(self._cardDeck.getNumOfCardsInDeck()):
            super().add(self._cardDeck.viewCardAt(i))

    def __startNewRound(self):
        """  Starts a new round of poker (a new round of betting)  """

        self._winner = "No Winner"
        self._userHand = "None"
        self._computerHand = "None"

        self._currentPot = 0
        self._currentWager = self._MINIMUM_BET_WAGE
        self._currentBeingRisked = 0

        self.__hideAllDisplayedCards()
        self._roundHasEnded = False
        self._userFolded = False

        self._cardsInDisplay = 0
        self._cardDeck.addAllCardsBackIntoDeck()
        self._cardDeck.shuffle()

        self._userCard1 = self._cardDeck.getCardFromDeck()
        self._userCard2 = self._cardDeck.getCardFromDeck()
        self._computerCard1[0] = self._cardDeck.getCardFromDeck()
        self._computerCard2[0] = self._cardDeck.getCardFromDeck()

        self._userCard1.displayCardAtGivenPos(40, 365)
        self._userCard2.displayCardAtGivenPos(152, 365)
        self._computerCard1[1].displayCardAtGivenPos(376, 115)
        self._computerCard2[1].displayCardAtGivenPos(488, 115)

    def __hideAllDisplayedCards(self):
        """  Hides all of the five display cards in the middle of the window from the user  """

        self._userCard1.hideCard()
        self._userCard2.hideCard()
        self._computerCard1[0].hideCard()
        self._computerCard2[0].hideCard()
        self._computerCard1[1].hideCard()
        self._computerCard2[1].hideCard()

        for i in range(5):
            self._displayCards[i].hideCard()

    def __displayFlop(self):
        """  Displays the first three cards of the 5-card set  """

        self._currentWager = self._MINIMUM_BET_WAGE  # The wager goes back to the minimum value after each new card flip
        positions = [(40, 240), (152, 240), (264, 240)]

        for i in range(3):
            self._displayCards[i] = self._cardDeck.getCardFromDeck()
            self._displayCards[i].displayCardAtGivenPos(positions[i][0], positions[i][1])

        self._cardsInDisplay = 3

    def __displayFourthCard(self):
        """  Displays the fourth card of the 5-card set  """

        self._currentWager = self._MINIMUM_BET_WAGE  # The wager goes back to the minimum value after each new card flip
        self._displayCards[3] = self._cardDeck.getCardFromDeck()
        self._displayCards[3].displayCardAtGivenPos(376, 240)
        self._cardsInDisplay = 4

    def __displayLastCard(self):
        """  Displays the last card of the 5-card set  """

        self._currentWager = self._MINIMUM_BET_WAGE  # The wager goes back to the minimum value after each new card flip
        self._displayCards[4] = self._cardDeck.getCardFromDeck()
        self._displayCards[4].displayCardAtGivenPos(488, 240)

        self._cardsInDisplay = 5

    def __displayFaceValueComputerCards(self):
        """  Displays the face value of the computer's two cards  """

        self._computerCard1[1].hideCard()
        self._computerCard2[1].hideCard()
        self._computerCard1[0].displayCardAtGivenPos(376, 115)
        self._computerCard2[0].displayCardAtGivenPos(488, 115)

    def keyDown(self, key):
        """
        This function is called whenever a key is pressed
        :param key: the key that was pressed
        """
        if (key == pygame.K_RETURN or key == pygame.K_q) \
                and (self._startTime == -1 or (time.time() - self._startTime > 0.05)):
            self.__fold()
            self._startTime = time.time()

    def mouseButtonDown(self, x, y):
        """
        This function is called whenever the mouse button is clicked
        :param x: the x-coordinate of the mouse
        :param y: the y-coordinate of the mouse
        """
        # You can't execute a turn when it's the computer's turn
        if self._computerHasTurn:
            return

        if not self._roundHasEnded:
            if self._foldButton.mouseIsOver(pygame.mouse.get_pos()) and self._foldButton.isClickable():
                self.__fold()
            elif self._callButton.mouseIsOver(pygame.mouse.get_pos()) and self._callButton.isClickable():
                self.__call()
            elif self._raiseButton.mouseIsOver(pygame.mouse.get_pos()) and self._raiseButton.isClickable():
                self.__raise()
        else:
            if self._newRoundButton.mouseIsOver(pygame.mouse.get_pos()) and self._newRoundButton.isClickable():
                self.__startNewRound()
            elif self._exitGameButton.mouseIsOver(pygame.mouse.get_pos()) and self._exitGameButton.isClickable():
                super().quit()

    def __fold(self):
        """  Simulates the user folding in Texas Hold 'em, where all money in the pot goes to the computer  """

        self._computerMoney += self._currentPot

        self._currentPot = 0
        self._currentWager = self._MINIMUM_BET_WAGE
        self._currentBeingRisked = 0

        self.__updateTextData()
        self._roundHasEnded = True
        self._winner = "Computer"
        self._userFolded = True

        self.__displayFaceValueComputerCards()
        self._userHand = self.checkHand(True)
        self._computerHand = self.checkHand(False)

        if self._cardsInDisplay == 0:
            self.__displayFlop()

        if self._cardsInDisplay == 3:
            self.__displayFourthCard()

        if self._cardsInDisplay == 4:
            self.__displayLastCard()

    def __call(self):
        """  Simulates the user placing a 'call' in Texas Hold 'em  """

        # True if the user runs out of money
        if self._userMoney - self._currentWager < 0:  # Starts the game over from scratch
            self._userMoney = self._START_BALANCE
            self._computerMoney = self._START_BALANCE
            self._currentPot = 0
            self._currentBeingRisked = 0
            self.__fold()
            return

        self._userMoney -= self._currentWager
        self._currentPot += self._currentWager
        self._currentBeingRisked += self._currentWager

        self.__updateTextData()
        self.__executeComputerCall()

        # True if this is the last bet that will be placed - A winner will now be determined
        if self._cardsInDisplay == 5:
            self.__displayFaceValueComputerCards()
            self._userHand = self.checkHand(True)
            self._computerHand = self.checkHand(False)
            self.determineWinner()

    def __raise(self):
        """  Simulates the user executing a 'raise', where the bet gets raised  """

        if self._userMoney < 2 * self._currentWager:
            return

        self._currentWager *= 2

        self._userMoney -= self._currentWager
        self._currentPot += self._currentWager
        self._currentBeingRisked += self._currentWager

        self.__updateTextData()
        self.__executeComputerCall()

        if self._cardsInDisplay == 5:
            self.__displayFaceValueComputerCards()
            self._userHand = self.checkHand(True)
            self._computerHand = self.checkHand(False)
            self.determineWinner()

    def __executeComputerCall(self):
        """  Allows the computer to execute a call - The computer always matches whatever bet the user makes  """

        self._computerMoney -= self._currentWager
        self._currentPot += self._currentWager
        self._computerHasTurn = True
        self._computerTurnStartTime = time.time()

    def __displayComputerTurnText(self):
        """  Displays some text that let's the user know that it's currently the computer's turn - Enhances gameplay """

        font = pygame.font.SysFont("Arial", 15)
        if self._userHand == "None":
            text = font.render("Computer is making a move...", True, (161, 29, 70))
            super().getDisplay().blit(text, (50, 75))

    def determineWinner(self):
        """  Determines who the winner is after no more bets are being placed (Who has the best hand)  """

        # The card names, in order of lowest to highest score
        aList = Deck.TYPES[1:] + ["Ace"]

        # The higher the score, the higher the high-card
        userCardScore = aList.index(PokerGame.getHighCard([self._userCard1, self._userCard2]))
        compCardScore = aList.index(PokerGame.getHighCard([self._computerCard1[0], self._computerCard2[0]]))

        # if the userScore is positive, then the lowest user score is the winner - Same goes for the computer score
        if self._userHand in self._CARD_HANDS:
            userScore = self._CARD_HANDS.index(self._userHand)
        else:
            userScore = -1  # True if the user didn't have any card hand

        if self._computerHand in self._CARD_HANDS:
            computerScore = self._CARD_HANDS.index(self._computerHand)
        else:
            computerScore = -1

        # If the user or computer score is -1, then the high card is executed as the best hand
        if userScore >= 0 and computerScore >= 0:
            if userScore < computerScore:
                self._winner = "User"
            elif userScore > computerScore:
                self._winner = "Computer"
            elif userCardScore > compCardScore:
                self._winner = "User"
            elif userCardScore < compCardScore:
                self._winner = "Computer"
            else:
                self._winner = "Nobody"
        elif userScore == -1 and computerScore == -1:
            if userCardScore > compCardScore:
                self._winner = "User"
            elif userCardScore < compCardScore:
                self._winner = "Computer"
            else:
                self._winner = "Nobody"
        elif userScore == -1:
            self._winner = "Computer"
        else:
            self._winner = "User"

        if self._winner == "User":
            self._userMoney += self._currentPot
        elif self._winner == "Computer":
            self._computerMoney += self._currentPot
        else:
            self._userMoney += self._currentPot/2
            self._computerMoney += self._currentPot/2

        self._currentPot = 0
        self._currentWager = self._MINIMUM_BET_WAGE
        self._currentBeingRisked = 0

        self.__updateTextData()
        self._roundHasEnded = True

    def displayWinner(self):
        """  Displays the winner as text being blitted to the screen  """

        font = pygame.font.SysFont("Arial", 15)

        if self._userFolded:
            text = font.render("Since you folded, " + self._winner + " wins the pot!", True, (161, 29, 70))
        else:
            text = font.render(self._winner + " wins!", True, (161, 29, 70))

        text2 = font.render("Your best hand: " + self._userHand, True, (161, 29, 70))
        text3 = font.render("Computer's best hand: " + self._computerHand, True, (161, 29, 70))
        super().getDisplay().blit(text, (50, 75))
        super().getDisplay().blit(text2, (50, 95))
        super().getDisplay().blit(text3, (50, 115))

    def __updateTextData(self):
        """  Updates the text data which is displayed on the bottom right of the window  """

        font = pygame.font.SysFont("Arial", 15)

        text1 = font.render("Minimum Wager: $" + str(self._MINIMUM_BET_WAGE), True, pygame.color.Color('#ffffff'))
        text2 = font.render("Current Wager: $" + str(self._currentWager), True, pygame.color.Color('#ffffff'))
        text3 = font.render("Amount at Risk: $" + str(self._currentBeingRisked), True, pygame.color.Color('#ffffff'))
        text4 = font.render("Current pot: $" + str(self._currentPot), True, pygame.color.Color('#ffffff'))
        text5 = font.render("Available Balance: $" + str(self._userMoney), True, pygame.color.Color('#ffffff'))
        text6 = font.render("Computer Balance: $" + str(self._computerMoney), True, pygame.color.Color('#ffffff'))

        self._textData = [text1, text2, text3, text4, text5, text6]

    def __blitTextData(self):
        """  Blits all of the text data which is displayed on the bottom right of the window  """

        locations = [(250, 280), (250, 300), (250, 330), (250, 350), (425, 280), (425, 300)]

        # Both values should always be equal, but just in case...
        if len(self._textData) < len(locations):
            count = len(self._textData)
        else:
            count = len(locations)

        # Blit all of the text in the text list
        for i in range(count):
            super().getDisplay().blit(self._textData[i], locations[i])

    def __displayButtonData(self):
        """  Displays the call, fold, and raise buttons on the window  """

        self._callButton.updateText("Call ($" + str(self._currentWager) + ")")
        self._raiseButton.updateText("Raise ($" + str(self._currentWager) + ")")

        self._foldButton.drawButton(super().getDisplay(), 15)
        self._callButton.drawButton(super().getDisplay(), 15)
        self._raiseButton.drawButton(super().getDisplay(), 12)

    def __displayGameOptions(self):
        """  Displays the two game option buttons (after a winner has been determined)  """

        self._newRoundButton.drawButton(super().getDisplay(), 10)
        self._exitGameButton.drawButton(super().getDisplay(), 12)

    def __checkForClickabilityChanges(self):
        """  Checks to see if the clickability of certain buttons needs to be changed  """

        # Buttons used for betting
        if self._userMoney < self._currentWager * 2:  # True if the user couldn't afford to raise the bet
            self._raiseButton.changeClickability(False, super().getDisplay(), 12)
        elif not self._raiseButton.isClickable() and self._userMoney >= self._currentWager * 2:
            self._raiseButton.changeClickability(True, super().getDisplay(), 12)

        # Buttons used to exit or start a new round
        if self._roundHasEnded and (not self._newRoundButton.isClickable() or not self._exitGameButton.isClickable()):
            self._newRoundButton.changeClickability(True, super().getDisplay(), 10)
            self._exitGameButton.changeClickability(True, super().getDisplay(), 12)
        elif not self._roundHasEnded and (self._newRoundButton.isClickable() or self._exitGameButton.isClickable()):
            self._newRoundButton.changeClickability(False, super().getDisplay(), 10)
            self._exitGameButton.changeClickability(False, super().getDisplay(), 12)

    def __displayNextCardSet(self):
        """  Displays the next card set in order of flop, fourth card, and last card  """

        if self._cardsInDisplay == 0:
            self.__displayFlop()
        elif self._cardsInDisplay == 3:
            self.__displayFourthCard()
        elif self._cardsInDisplay == 4:
            self.__displayLastCard()

    def checkHand(self, userHand):
        """
        Calculates what the user's or computer's best 5-card hand is out of a list of their seven cards
        :param userHand: True if the current card hand being checked is the user's. False, if it's the computer's hand
        :return: the highest hand available, or the highest card if no card hand is present
        """
        functions = ["isRoyalFlush", "isStraightFlush", "isFourOfAKind", "isFullHouse", "isFlush", "isStraight",
                     "isThreeOfAKind", "isTwoPairs", "isOnePair"]

        if userHand:  # True if the current card hand being checked is the user's
            cards = self._displayCards + [self._userCard1, self._userCard2]
        else:
            cards = self._displayCards + [self._computerCard1[0], self._computerCard2[0]]

        # Calls each function in the list with every possible 5-card combination from the seven cards
        for i in range(len(functions)):
            for j in range(len(cards)):  # 7 (Gets every 6-card combination)
                start, end = j, j + 6

                if end >= len(cards) + 1:
                    end = end - len(cards)
                    specificCards = cards[start:] + cards[:end]
                else:
                    specificCards = cards[start:end]

                for k in range(len(specificCards)):  # 6 (Gets every 5-card combination from every 6-card combination)
                    start, end = k, k + 5

                    if end >= len(specificCards) + 1:
                        end = end - len(specificCards)
                        temp = specificCards[start:] + specificCards[:end]
                    else:
                        temp = specificCards[start:end]

                    # This line is only needed to show that the temp variable is being used
                    variableName = [k for k, v in locals().items() if v == temp][0]

                    # One of the nine functions with a unique 5-card set gets called here
                    if eval("PokerGame." + functions[i] + "(" + variableName + ")"):
                        return self._CARD_HANDS[i]

        return PokerGame.getHighCard(cards[5:])

    @staticmethod
    def getHighCard(cards):
        """
        Gets the highest card found in the card deck.
        :param cards: a list of Card objects
        :return: the highest card in the deck (2 is the lowest, Ace is the highest)
        """
        cardRanking = Deck.TYPES[1:] + ["Ace"]

        for i in range(len(cardRanking) - 1, -1, -1):
            for j in range(len(cards)):
                if cardRanking[i] in cards[j].getCardName():
                    return cardRanking[i]

    @staticmethod
    def isFlush(cards):
        """
        Determines whether or not a specific card hand is a flush
        :param cards: a list of Card objects to be checked
        :return: whether or not the deck of cards contains a flush
        """
        cardNames = []
        for card in cards:
            cardNames.append(card.getCardName())

        letter = 'o'
        for i in range(len(cardNames)):
            for j in range(len(cardNames[i])):
                if cardNames[i][j] == 'C' or cardNames[i][j] == 'D' or cardNames[i][j] == 'H' or cardNames[i][j] == 'S':
                    if i == 0:
                        letter = cardNames[i][j]
                        break
                    elif letter != cardNames[i][j]:
                        return False

        return True

    @staticmethod
    def isStraight(cards):
        """
        Determines whether or not a specific card hand is a straight
        :param cards: a list of Card objects to be checked
        :return: whether or not the deck of cards contains a straight
        """
        temp = []
        for card in cards:
            temp.append(card.getCardName())

        aList = Deck.TYPES[1:] + ["Ace"]

        for i in range(len(temp)):
            for j in range(i + 1, len(temp)):
                v1, v2 = 0, 0

                for k in range(len(aList)):
                    if aList[k] == temp[i].split()[0]:
                        v1 = k

                for k in range(len(aList)):
                    if aList[k] == temp[j].split()[0]:
                        v2 = k

                if v1 > v2:
                    t = temp[j]
                    temp[j] = temp[i]
                    temp[i] = t

        # Takes care of the problem of the ace either being high or low
        if temp[4].split()[0] == "Ace" and temp[0].split()[0] == "Two":
            temp.pop(4)

        startListIndex = 0
        for k in range(len(aList)):
            if aList[k] == temp[0].split()[0]:
                startListIndex = k

        for i in range(1, len(temp)):
            if temp[i].split()[0] != aList[startListIndex + i]:
                return False

        return True

    @staticmethod
    def isRoyalFlush(cards):
        """
        Determines whether or not a specific card hand is a royal flush
        :param cards: a list of Card objects to be checked
        :return: whether or not the deck of cards contains a royal flush
        """
        temp = []
        for card in cards:
            temp.append(card.getCardName())

        needed = Deck.TYPES[9:] + ["Ace"]
        if not PokerGame.isFlush(cards):
            return False

        for value in temp:
            for i in range(len(needed)):
                if value.split()[0] == needed[i]:
                    needed[i] = "*"
                    break

        for s in needed:
            if s != "*":
                return False

        return True

    @staticmethod
    def isStraightFlush(cards):
        """
        Determines whether or not a specific card hand is a straight flush
        :param cards: a list of Card objects to be checked
        :return: whether or not the deck of cards contains a straight flush
        """
        return PokerGame.isFlush(cards) and PokerGame.isStraight(cards)

    @staticmethod
    def isXofAKind(cards, X):
        """
        Determines whether or not a specific card hand contains a certain number of the same cards
        :param cards: a list of card objects to be checked
        :param X: the number of consecutive cards that must exist, in order for this function to return True
        :return: whether or not the card hand contains X amount of the same cards
        """
        if X < 0 or X > 4:
            exit("Error - 'value' of a kind is too large or small")

        temp = []
        for card in cards:
            temp.append(card.getCardName())

        occurrences = [0] * len(Deck.TYPES)
        aList = Deck.TYPES[1:] + ["Ace"]

        # Gets the number of occurrences for each card
        for i in range(len(temp)):
            for j in range(len(aList)):
                if aList[j] == temp[i].split()[0]:
                    occurrences[j] += 1

        for i in range(len(occurrences)):
            if occurrences[i] == X:
                return True

        return False

    @staticmethod
    def isTwoPairs(cards):
        """
        Determines whether or not a specific card hand is a two-pair hand
        :param cards: a list of Card objects to be checked
        :return: whether or not the deck of cards contains two pairs of different cards
        """
        temp = []
        for card in cards:
            temp.append(card.getCardName())

        occurrences = [0] * len(Deck.TYPES)
        aList = Deck.TYPES[1:] + ["Ace"]

        for i in range(len(temp)):
            for j in range(len(aList)):
                if aList[j] == temp[i].split()[0]:
                    occurrences[j] += 1

        num = 0
        for i in range(len(occurrences)):
            if occurrences[i] == 2:
                num += 1

        return num == 2

    @staticmethod
    def isOnePair(cards):
        """
        Determines whether or not a specific card hand is a one-pair hand
        :param cards: a list of Card objects to be checked
        :return: whether or not the deck of cards contains two of the same cards
        """
        return PokerGame.isXofAKind(cards, 2)

    @staticmethod
    def isFourOfAKind(cards):
        """
        Determines whether or not a specific card hand is a four of a kind
        :param cards: a list of Card objects to be checked
        :return: whether or not the deck of cards contains four cards of the same type
        """
        return PokerGame.isXofAKind(cards, 4)

    @staticmethod
    def isFullHouse(cards):
        """
        Determines whether or not a specific card hand is a full house
        :param cards: a list of Card objects to be checked
        :return: whether or not the deck of cards contains a full house
        """
        return PokerGame.isXofAKind(cards, 3) and PokerGame.isXofAKind(cards, 2)

    @staticmethod
    def isThreeOfAKind(cards):
        """
        Determines whether or not a specific card hand is a three of a kind
        :param cards: a list of Card objects to be checked
        :return: whether or not the deck of cards contains three cards of the same type
        """
        return PokerGame.isXofAKind(cards, 3)

    def run(self):
        """  Runs the game and listens for any events  """

        self.__startNewRound()  # The first round of poker is started here

        # This loop continues while the window is still being displayed
        while True:
            # Ends the computer's turn after one second from the start of the computer's turn
            if self._computerHasTurn and time.time() - self._computerTurnStartTime > self._COMPUTER_WAIT_TIME:
                self.__displayNextCardSet()
                self._computerHasTurn = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    super().quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouseButtonDown(event.pos[0], event.pos[1])
                elif event.type == pygame.KEYDOWN:
                    self.keyDown(event.key)

            # Checks to see if the clickability of any buttons needs updating
            self.__checkForClickabilityChanges()

            # Update stuff and fill the window background
            super().update()
            GRAY = (30, 30, 30)

            super().getDisplay().fill(GRAY)
            super().draw()

            # Don't display the buttons during the short period when it's the computer's turn
            if not self._computerHasTurn and not self._roundHasEnded:
                self.__displayButtonData()
                self.__updateTextData()
            elif self._computerHasTurn:
                self.__displayComputerTurnText()  # Execute text when it's the computer's turn
            elif self._roundHasEnded:
                self.displayWinner()
                self.__displayGameOptions()

            # Displays other stuff on the canvas
            self.__blitTextData()

            pygame.display.flip()
            pygame.display.update()

            fps = super().getFramesPerSecond()
            super().getClock().tick(fps)
            super().updateTicks(1)

