''' GAME RULES

There are 77 cards in total. 
    - 2 Exploding Kitten Cards
    - 6 Defuse Cards
    - 8 Nope Cards
    - 7 Attack Cards
    - 7 Skip Cards
    - 7 Favor Cards
    - 7 Shuttle Cards
    - 8 See the Future Cards
    - 25 Cat Cards (5 of each of the following: TacoCat, )

'''

import random

class Player():
    def __init__(self, name, drawPile, discardPile):
        self.name = name
        self.drawPile = drawPile
        self.discardPile = discardPile
        self.hand = Hand()
        self.exploded = False
        self.playTurns = 0

    def takeTurn(self, previousCard=False):

        print(self.name + ' Turn ' + str(self.playTurns + 1) + ': ')

        choice = ''
        while (choice != 'pass' and not self.exploded):
            
            print('Here are your cards: ')
            self.hand.printNumberedCards()

            choice = input('Type one number of the card you want to play or type \'pass\' to end turn: ')
            if choice == 'pass':
                print('To pass, player will draw a card')
                self.drawCard()
                break
            elif choice.isnumeric() and int(choice) <= self.hand.size: #todo: add validation for too big of a number
                self.turnPlay(int(choice))
            else:
                print('Wrong Input... Please try again. \n')

    def turnPlay(self, cardNumber):
        card = self.hand.removeCardAt(cardNumber - 1)
        self.discardPile.addCard(card)

        print('Adding to Discard Pile...')
        self.discardPile.printNumberedCards()
        self.playTurns += 1
        card.play()
        return False

    def drawCard(self, printLog=True): #add card into hand
        card = self.drawPile.removeCard()
        if card:
            if printLog:
                print(self.name + ' has drawn a ...')
            if isinstance(card, ExplodingKittenCard):
                print('AN EXPLODING KITTEN CARD! OH NO!\n')
                if self.hand.defuses > 0:
                    print('Thankfully you have ' + self.hand.defuses + ' Defuse Cards! So we can use one and insert the exploding card back into the deck')
                    choice = input('Type one number between 1 and ' + str(self.drawPile.size) + ' of the position you want to insert the exploding kitten or type \'random\': ')
                    if choice.isnumeric() and int(choice) <= self.hand.size: #todo: add validation for too big of a number
                        self.hand.removeCard() # removes the first card which will be the card that you most recently drawn
                        self.drawPile.addCardAt(card, int(choice) - 1)
                    elif choice == 'random':
                        self.drawPile.insertRandomExplodingKitten()
                    else:
                        print('Wrong Input... Please try again. \n')
                else:
                    self.exploded = True
                    print('Unfortunately you have no more Defuse cards')
            else:
                if printLog:
                    print(card.name + '\n')
                self.hand.addCard(card)

class LinkedCards():
    def __init__(self,
            exploding, defuse, skip, favor, shuffle, future, cat
        ):
        self.cardtypesmap = {
            'exploding': exploding,
            'defuse': defuse,
            'skip': skip,
            'favor': favor,
            'shuffle': shuffle,
            'future': future,
            'cat': cat
        }

        self.head = None
        self.size = 0

    def addCard(self,card):
        card.next = self.head
        self.head = card
        self.size += 1

    def addCardAt(self, card, addIndex):
        if addIndex == 0:
            return self.addCard(card)

        current = self.head
        currentIndex = 0

        while current and currentIndex <= (addIndex - 2):
            current = current.next
            currentIndex += 1
        
        nextNextCard = current.next
        current.next = card
        current.next.next = nextNextCard

        self.size += 1

    def removeCard(self):
        card = self.head
        if not card:
            return None
        self.head = self.head.next
        card.next = None #detach rest of linked cards from card
        self.size -=1 
        return card

    def removeCardAt(self, removeIndex):
        if removeIndex == 0:
            return self.removeCard()

        current = self.head
        currentIndex = 0

        while current and currentIndex <= (removeIndex - 2):
            current = current.next
            currentIndex += 1
        
        card = current.next
        current.next = current.next.next
        card.next = None #detach rest of linked cards from card
        self.size -=1 
        return card
    
    def getCardList(self):
        cardList = []
        current = self.head
        while current:
            cardList.append(current)
            current = current.next
        return cardList

    def printNumberedCards(self):
        current = self.head
        num = 1
        if not current:
            print('There are no cards')
        while current:
            print(num, ':', current.name)
            current = current.next
            num += 1
        
        print('\n')

class Hand(LinkedCards):
    def __init__(self, *args):
        self.head = DefuseCard() #default hand has a defuse card
        self.size = 1
        self.iditer = 1
        self.defuses = 1
    
    def addCard(self,card):
        super().addCard(card)
        if isinstance(card, DefuseCard):
            self.defuses += 1

    def addCardAt(self, card, addIndex):
        super().addCardAt(card, addIndex)
        if isinstance(card, DefuseCard):
            self.defuses += 1

    def removeCard(self):
        card = super().removeCard()
        if isinstance(card, DefuseCard):
            self.defuses -= 1
        return card

    def removeCardAt(self, removeIndex):
        card = super().removeCardAt(removeIndex)
        if isinstance(card, DefuseCard):
            self.defuses -= 1
        return card
        

class DiscardPile(LinkedCards):
    def __init__(self, *args):
        super().__init__(0,0,0,0,0,0,0)
        self.lastPlayedCard = None

    def addCard(self, card):
        super().addCard(card)
        self.lastPlayedCard = card

class DrawPile(LinkedCards):
    def __init__(self, *args):
        super().__init__(0,8,11,11,11,11,11)
        self.create()

    def create(self):

        def shuffleDeck(deck):
            print('Draw pile is being shuffled\n')
            deck.shuffle()
            
        def seeTheFuture(deck):
            print('Here are the top 3 cards of the draw pile: ' + ' -> '.join(deck.peek()) + '\n')

        totalList = []
        totalList += [DefuseCard() for _ in range(self.cardtypesmap['defuse'])]
        totalList += [SpecialCard(shuffleDeck, self, 'shuffle','Shuffle') for _ in range(self.cardtypesmap['shuffle'])]
        totalList += [SpecialCard(seeTheFuture, self, 'future','See The Future') for _ in range(self.cardtypesmap['future'])]
        totalList += [CatCard('taco','Taco Cat') for _ in range(self.cardtypesmap['cat'])]
        totalList += [CatCard('beard','Beard Cat') for _ in range(self.cardtypesmap['cat'])]
        totalList += [CatCard('cattermelon','Cattermelon') for _ in range(self.cardtypesmap['cat'])]

        random.shuffle(totalList)
        for card in totalList:
            super().addCard(card)


    def shuffle(self):
        randomCardList = self.getCardList()
        random.shuffle(randomCardList)
        self.head = None

        for card in randomCardList:
            self.addCard(card)
        return self.head

    def peek(self, top=3):
        #default show top 3 cards
        peekList = []
        current = self.head
        while current and top > 0:
            peekList.append(current.name)
            current = current.next
            top -= 1
        
        return peekList

    def insertRandomExplodingKitten(self):
        randIndex = random.randint(0, self.size-1)
        index = 0
        current = self.head
        while index < randIndex and current:
            current = current.next
            index += 1

        nextLinkedCards = current.next
        current.next = ExplodingKittenCard()
        current.next.next = nextLinkedCards
        self.size += 1
        return index, current.next

class Card():
    def __init__(self, cardType, cardName):
        self.type = cardType
        self.name = cardName
        self.next = None

    def play(self):
        print('Playing ', self.name, ' Card...')

class ExplodingKittenCard(Card):
    def __init__(self, *args):
        super().__init__('exploding', 'Exploding Kitten')

class DefuseCard(Card):
    def __init__(self, *args):
        super().__init__('defuse', 'Defuse')
    
    def play(self):
        super().play()
        print('How silly to play this card! Its a useful protection card but you play what you want to play...')

class CatCard(Card):
    def __init__(self, *args):
        super().__init__('cat', 'Cat')

class SpecialCard(Card):
    def __init__(self, func, deck, *args):
        super().__init__(*args)
        self.special = func
        self.deck = deck

    def play(self):
        super().play()
        self.special(self.deck)

class ExplodingKittensXtremeGame():
    def __init__(self):
        self.gameOn = True
        self.draw = DrawPile()
        self.discard = DiscardPile()

        self.playerOne = Player('Player 1', self.draw, self.discard)
        self.playerTwo = Player('Player 2', self.draw, self.discard)

        #players dealt cards
        dealCardsIter = 1
        while dealCardsIter < 25:
            self.playerOne.drawCard(False)
            self.playerTwo.drawCard(False)
            dealCardsIter += 1

        #insert exploding kittens randomly
        self.draw.insertRandomExplodingKitten()
        self.draw.insertRandomExplodingKitten()

        self.showInstructions()
        self.askToPlayGame()

    def showInstructions(self):
        print('Welcome to Exploding Kittens EXTREME. Each player will be dealt 25 cards, ensuring you both have exactly 1 Defuse card in your initial hand')
        print('Each player will have a chance to look at their hand before they...')
        print('1. Pass (play no cards)')
        print('2. or Play (following the instructions of a card you take from your hand and add to the Discard Pile')
        print('End the turn by drawing a card from top of Draw Pile')
        print('The last player who has not exploded wins the game')
        print('\n')
    
    def invalidInput(self):
        print('That is not a valid input.')
        print('\n')
    
    def askToPlayGame(self, post='now'):
        while True:
            print('Would you like to play the game ' + post + '? Type \'yes\' to play, \'no\' to end, \'instructions\' to read the instructions')
            choice = input('Please enter choice: ')
            if choice == 'yes':
                print('Game starting...')
                self.loopGame()
                break
            elif choice == 'no':
                print('Game ending...')
                break
            elif choice == 'instructions':
                print('\n')
                self.showInstructions()
            else:
                print('\n')
                self.invalidInput()

    def loopGame(self):
        print('Cards have been dealt to ' + self.playerOne.name + ' and ' + self.playerTwo.name)
        print('\n')

        while not self.playerOne.exploded and not self.playerTwo.exploded and self.gameOn: 
            self.playerOne.takeTurn()

            if self.playerOne.exploded:
                self.gameOn = False
                print(self.playerTwo.name + ' wins!')
                print('\n')
                self.askToPlayGame('again')
                break

            self.playerTwo.takeTurn()
        
        if self.playerTwo.exploded:
            self.gameOn = False
            print(self.playerOne.name + ' wins!')
            print('/n')
            self.askToPlayGame('again')

ExplodingKittensXtremeGame()