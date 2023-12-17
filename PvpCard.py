from DreamEnums import PvpCardType

class PvpCard:  #builds Pvp_Cards class
    def __init__(self, type, player_owner):
        self.type = type    #Mom says hang up. share a secret, speakerphone.
        self.player_owner = player_owner  #who played the card
        self.used_on = [] #what Card the Pvp_Card was used on
        #self.long_name = long_name #a way to not have to type shit every time)