class Player:  #class Player constructor
    def __init__(self, playernumber):
        self.playernumber = playernumber    #Class Player gets a "playernumber" attribute
        self.cardsinhand = []               #Class Player gets a "cardsinhand" attribute
        self.playername = ""                #gives players a name attribute in the class
        self.collected_clues = []           #where the information goes that the player collects
        self.dialed_this_turn = False       #a flag for limiting 1 dial per turn
        self.guessed_this_turn = False      #only one guess per turn flag
        self.pvp_in_hand = []
        self.pvp_this_turn = False

    # Reset all turn-based flags
    def end_turn(self):
        self.dialed_this_turn = False
        self.guessed_this_turn = False
        self.pvp_this_turn = False

    # Prints players' hand; both "Boy" card and PvP cards
    def print_hand(self): 
        print(f"{self.playername}'s current hand is")
        for i in self.cardsinhand:
            print(f"{i.name} - Phone#: {i.phonenum}")

        print("PvP", end = " ")
        for i in self.pvp_in_hand:
            print(f"|{i.type}|", end = " ")
        print(end = "\n")

    def print_pvp_cards(self):
        for i in self.pvp_in_hand:
            print(f"{self.pvp_in_hand.index(i)} - |{i.type}|")