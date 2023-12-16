import json

class Card:  #class Card constructor
    def __init__(self, name, phonenum, hangout, sport, food, clothing, clue_to_reveal, first_call, curse_bucket):
        self.name = name    #Class Cards gets a "name" attribute
        self.phonenum = phonenum  #Card objects have stuff
        self.hangout = hangout
        self.sport = sport
        self.food = food
        self.clothing = clothing
        self.clue_to_reveal = clue_to_reveal #this is where the clues that are revealed in the game assoicate with cards to dial
        self.first_call = first_call #a flag to show if the card has been dialed before
        self.curse_bucket = curse_bucket #where pvp cards can haunt boy cards

# Decoder to turn JSON into Card objects
class CardDecoder(json.JSONDecoder):
    def __init__(self, object_hook = None, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)
                         
    def object_hook(self, o):
        decoded_card =  Card(
            o.name('name'),
            o.phonenum('phonenum'),
            o.hangout('hangout'),
            o.sport('sport'),
            o.food('food'),
            o.clothing('clothing'),
            o.clue_to_reveal('clue_to_reveal'),
            o.first_call('first_call'),
            o.curse_bucket('curse_bucket')
        )