# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 16:24:42 2017

@author: nedd
"""
import random

class Deck():
    def __init__(self, cards = []):
        if len(cards) ==0:
            self.cards = self.makeBaseCards()
        else:
            self.cards = cards
        self.discards =[]
        self.Shuffle()
        
    def Shuffle(self):
        self.cards += self.discards
        self.discards = []
        random.shuffle(self.cards)
    
    def drawSingleCard(self):
        new_card = self.cards.pop()
        return new_card
        
    @staticmethod
    def makeBaseCards():
        values = [-2,-2,-1,-1,-1,0,0,0,0,1,1,1,2,2,0,0]
        multiples = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,2]
        reshuffle = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,True,True]
        cards = []
        for i in range(len(values)):
            cards.append(Card(values[i],multiple=multiples[i], reshuffle=reshuffle[i]))
            
        return cards
        
    def addCurse(self):
        curse = Card(0, multiple=0, reshuffle=True, remove=True)
        self.addCard(curse)
        
    def addCard(self, card):
        self.cards.append(card)
        
    def addBless(self, card):
        bless = Card(0, multiple=2, reshuffle=True, remove=True)
        self.addCard(bless)
        
        
    def Draw(self):
        cards = []
        new_card = self.drawSingleCard()
        cards.append(new_card)
        while new_card.rolling:
            new_card = self.drawSingleCard()
            cards.append(new_card)
        return cards
        
    def makeAttack(self, power = 2, advantage = 0):
        all_cards =[]
        cards = self.Draw()       
        all_cards += cards
        r1 = Results(cards, power)
        if advantage ==1:
            cards2 = self.Draw()
            all_cards += cards2
            r2 = Results(cards2,power)
            if  r1> r2:
                return r1, all_cards
            else:
                return r2, all_cards
        elif advantage == -1:
            cards2 = self.Draw()
            all_cards += cards2
            r2= Results(cards2, power)
            if r2 > r1:
                return r1, all_cards
            else:
                return r2, all_cards
        
        else:
            return r1, all_cards
            
                    
    def cleanUp(self, cards):
        new_discards = []
        shuffle = False
        for card in cards:
            shuffle | card.reshuffle
            if not(card.remove):
                new_discards.append(card)
        self.discards += new_discards
        if shuffle:
            self.shuffle()
            
    def doTurn(self, power = 2):
        results, discards = self.makeAttack()
        self.cleanUp(discards)
        return results
        
    
class Card():
    def __init__(self, value, rolling = False, multiple = 1, modifiers = {}, reshuffle = False, remove = False):
        self.value = value
        self.rolling = rolling
        self.multiple = multiple
        self.modifiers = modifiers
        self.reshuffle = reshuffle
        self.remove = remove
        
    def __repr__(self):
        output = ""
        output += str(self.value) + " "
        output += "x "+str(self.multiple) + " "
        output += "rolling: " + self.rolling + " "
        output += self.modifiers
        return output

    def __str__(self):
        output = ""
        output += str(self.value) + " "
        output += "x "+str(self.multiple) + " "
        output += "rolling: " + self.rolling + " "
        output += self.modifiers
        return output
    
    
class Results():
    def __init__(self, base_power=2, cards=[]):
        self.cards = cards
        self.base_power = base_power
    def __gt__(self, other):
        mine = self.getResults()
        theirs = other.getResults()
        if not(isinstance(other, Results)):
            raise ValueError
        if mine['value']*mine['multiplier'] > theirs['value']*theirs['multiplier']:
            return True
        elif mine['value']*mine['multiplier'] < theirs['value']*theirs['multiplier']:
            return False
        else:
            if len(mine['modifiers']) > len(theirs['modifiers']):
                return True
            else:
                return False
                
    def __lt__(self, other):
        mine = self.getResults()
        theirs = other.getResults()
        if not(isinstance(other, Results)):
            raise ValueError
        if mine['value']*mine['multiplier'] < theirs['value']*theirs['multiplier']:
            return True
        elif mine['value']*mine['multiplier'] > theirs['value']*theirs['multiplier']:
            return False
        else:
            if len(mine['modifiers']) < len(theirs['modifiers']):
                return True
            else:
                return False
                
    def getResults(self):
        value = self.base_power
        total_multiplier=1
        modifiers ={}
        for card in self.cards:
            value += card.value
            total_multiplier = total_multiplier*card.multiple
            if len(card.modifiers) !=0:
                for key in card.modifiers.keys():
                    if key in modifiers.keys():
                        modifiers[key]+=card.modifiers[key]
                    else:
                        modifiers[key] = card.modifiers[key]
            
        return {'value': value, 'multiplier': total_multiplier, 'modifiers': modifiers}
        