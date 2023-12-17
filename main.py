import random
import copy
import time
import json
from types import SimpleNamespace
from DreamEnums import ClueType, PvpCardType
from Player import Player
from Card import Card
from PvpCard import PvpCard

from prettytable import PrettyTable    #this helps build BOY ATTRIBUTE TABLE
import colorama #fixes windows shell color bugs
from colorama import Fore, Back, Style #gives us come color options
### installing colorama: pip install colorama
### installing prettytable: python -m pip install -U prettytable
import click # Import click library for good screen clearing function
colorama.init() #turns on windows shell fix

all_player_list = [Player(1), Player(2), Player(3), Player(4)]  #all possible players in the game
current_player = all_player_list[0]     # Assign current player to player1 by default (can be changed later)
player_list = []  #a list built out by the player's choice of player num
crush = 0  #initalizes game crush global var

#building Card objects; load from file
with open("./cards.json") as f:
    card_json_data = json.load(f)
    card_list = [Card(**k) for k in card_json_data]

##global stuff
# this is the master list of cards in the deck. a way to reference a var list containing all card object names.
# tried to find a less brute force way to do this but so far no luck.

game_deck = copy.copy(card_list)  # this clones from the master list for the "in game" deck. Use game_deck when moving stuff around, use card_list as universal master ref)
in_hand = []  # initializes player hand as empty
discard_pile = []  # initializes discard pile as empty

#functions
def clear_screen():
    # Clear screen using click.clear() function
    click.clear()

#Text Speed Delay Settings
def delay():
    time.sleep(1)

def short_delay():
    time.sleep(.5)

def long_delay():
    time.sleep(2)

#Some TEXT STYLE stuff
def blue_out(text): #red_out is how i am crossing out entries in the notepad
    return Back.LIGHTBLACK_EX + Fore.BLUE + text + Style.RESET_ALL

def red_out(text): #red_out is how i am crossing out entries in the notepad
    return Back.RED + Fore.WHITE + text + Style.RESET_ALL

def white_out(text): #red_out is how i am crossing out entries in the notepad
    return Back.WHITE + Fore.BLACK + text + Style.RESET_ALL

def boy_attribute_table():   #this is an automated notepad of the clues you have crossed off the list. player specific
    notepad = PrettyTable(["Called?", "Hangout", "Sport / Food", "Clothing", "Secret Admirer?"]) # Specify the Column Names while initializing the Table
    for i in card_list:   #iterates over all cards
        hangout = i.hangout
        sport = i.sport
        food = i.food
        clothing = i.clothing
        name = i.name
        listname = i.name
        if i in current_player.collected_clues: name = red_out(i.name) #reds out a name you have dialed already in the "dialed" list
        for x in current_player.collected_clues: #iterates over all the clues the player has heard so far
            if x.clue_to_reveal == i.sport: sport = red_out(i.sport)
            if x.clue_to_reveal == i.hangout: hangout = red_out(i.hangout)
            if x.clue_to_reveal == i.food: food = red_out(i.food)
            if x.clue_to_reveal == i.clothing: clothing = red_out(i.clothing)   #if any of the clues collected fit in the category, it gets redded out
        if i.sport == None: sport = ""
        if i.food == None: food = ""   #removing null entries for food sport weirdness
        notepad.add_row([name,hangout, sport+food, clothing, listname])   #adds rows qeued up for printing
    notepad.align="l"   #aligns the table to the left
    clear_screen()
    print(notepad)  #prints notepad
    input("Press Enter to continue...")
    clear_screen()

def new_game_crush():
    clue_list = []  # makes bucket to hold all valid clues in
    crush = random.randint(0, int(len(card_list)-1)) #rng a boy from the card list to be the crush, adjusting len from starting at 1 while list index starts at 0
    for i in range (len(card_list)):   #creates a list of all possible clues in clue_list, removing "null" entries for foodsport wierdness
        if card_list[i].hangout != None: clue_list.append(card_list[i].hangout)
        if card_list[i].sport != None: clue_list.append(card_list[i].sport)
        if card_list[i].food != None: clue_list.append(card_list[i].food)
        if card_list[i].clothing != None: clue_list.append(card_list[i].clothing)

    clue_list = list(set(clue_list)) #removes all duplicate entries from the list
    random.shuffle(clue_list)  #shuffles clue list

    for i in range(len(clue_list)):   #distributes all clues to all cards' "clue to reveal" player object attribute
        card_list[i].clue_to_reveal = clue_list[i]
    return crush

def starting_deal():
    for i in range (3): #gives players 3 deck cards
        for f in player_list:
            f.cardsinhand.append(game_deck.pop(0))

    # Assign PVP cards; none in 1-player mode, one of each type in > 1 player mode
    if len(player_list) == 1: 
        print("Single Player Mode. PvP Cards Disabled.\nYou have drawn 3 cards from the deck.")
    else:
        for player in all_player_list:
                player.pvp_in_hand.append(PvpCard(PvpCardType.HANG_UP, player))
                player.pvp_in_hand.append(PvpCard(PvpCardType.SHARE_SECRET, player))
                player.pvp_in_hand.append(PvpCard(PvpCardType.SPEAKERPHONE, player))

        print("All Players have drawn 3 boy cards from the deck,\nand have 3 PvP cards in hand.")
        print("Starting Game...")
        delay()
        delay()
        clear_screen()

def check_decks():
    if len(game_deck) == 0: reshuffle()

def whos_turn(player):
    print(f"\n{Back.LIGHTBLACK_EX + Fore.BLUE}It is {player.playername}'s turn (Player {player.playernumber}).{Style.RESET_ALL}\n")

def set_number_of_players():
    print("How many players would like to play (1 - 4)?")
    while True:
        try:
            num = int(input())
            print(f"\nYou have selected {num} player{'s'[:num^1]}.")
            delay()
            number_of_players = int(num)
            for i in range(number_of_players):
                player_list.append(all_player_list[i])
            return number_of_players
        except: print("Please enter ('1', '2', '3' or '4') to select number of players.")

def name_players():
    for i in player_list:
        print(f"\nPlease give Player {i.playernumber} a name.")
        name = input()
        i.playername = name

    print("\nThe names you have chosen are:")
    short_delay()
    for i in player_list:
        print(f"Player {i.playernumber}, {i.playername}")
        short_delay()

def starting_player():
    if len(player_list) == 1:  #checks for one player mode
        return player_list[0]
    
    while True:
        print(f"\nPlease choose the starting player by entering their player number.")
        options = ["one", "two", "three", "four"]

        choice = input()
        if choice.lower() in options:
            choice = options.index(choice) - 1
        elif choice.isdigit():
                choice = int(choice)
                print(f"Player {choice} will go first.")
                short_delay()
                return player_list[choice - 1]      # Arrays are 0-based, so subtract one from choice
        else: 
            print("Not a valid choice.")

def check_for_curse(last_dialed_boy):
    if len(last_dialed_boy.curse_bucket) > 0:
        print(f"\nOh no! {last_dialed_boy.curse_bucket[0].player_owner.playername} "
          f"(Player {last_dialed_boy.curse_bucket[0].player_owner.playernumber}) has cursed your {last_dialed_boy.name} card with {last_dialed_boy.curse_bucket[0].type}!\n")
        long_delay()

        for i in last_dialed_boy.curse_bucket:
            match i.type:
                case PvpCardType.HANG_UP:
                    print(Back.RED + Fore.WHITE, f"You must discard your {last_dialed_boy.name} and lose a turn.",Style.RESET_ALL,"\n")
                case PvpCardType.SHARE_SECRET:
                    print(Back.RED + Fore.WHITE, f"Your revealed clue from {last_dialed_boy.name,} will also be added to their notepad. However, you will gain possession of their expended {i.type} PvP card.", Style.RESET_ALL, "\n")
                case PvpCardType.SPEAKERPHONE:
                    print(Back.RED + Fore.WHITE, f"Your revealed clue from {last_dialed_boy.name} will also be added to every player's notepad.",Style.RESET_ALL,"\n")

            long_delay()
            long_delay()

            return i.type

def use_pvp():   #this one is crazy
    ###checks that the player can use PVP###
    if len(player_list) == 1: # halt unless at least a 2 player game
        print("You cannot use PvP Cards in a 1 player game.")
        return

    if current_player.pvp_this_turn: #halt if you have used a pvp card already this turn
        print("Cannot use more than one PvP card per turn.")
        return
    else:
        if len(current_player.pvp_in_hand) != 0:  #checks that hand is not empty
            print("Please select a PvP card to use (number input), or ('exit') to leave.")
        else:
            print("You have no PvP Cards to use.")
            return

    opponent_list = copy.copy(player_list)
    opponent_list.remove(current_player)   #we need a list of players that doesn't include current player
    op_player_nums = []
    for i in opponent_list: op_player_nums.append(int(i.playernumber))  # making a bucket of all valid opponent player numbers
    op_player_names = []
    for i in opponent_list: op_player_names.append(i.playername)  # making a bucket of all valid opp player names
    op_player_names = [element.lower() for element in op_player_names]

    ###chosing a pvp card###
    current_player.print_pvp_cards()

    valid_choice = False
    while valid_choice == False:  #loop that only breaks when valid choice in made
        choice = input()
        if choice == 'exit':   #leaves pvp
            print("\nExiting PvP.")
            return
        if choice.isdigit():   #filters for num input
            if int(choice) not in range(int(len(current_player.pvp_in_hand))):  #if it's a num but not a possible correct one
                print("Entered number not in range of valid choices, try again.")   #print error
            for i in current_player.pvp_in_hand:   #iterate over your pvp hand
                if int(choice) == int(current_player.pvp_in_hand.index(i)):   #checks input against pvp cards
                    selected_pvp = current_player.pvp_in_hand[int(choice)]   #sets choice as var selected_pvp
                    print(f"\nYou chose |{selected_pvp.type}|\n")
                    valid_choice = True
                    break
        else: print("Please enter selection as a number. Try again.")

    ###chosing a player to use card on###
    print(f"Choose a player to curse with {selected_pvp.type}. Type name or number, or ('exit') to leave.")
    for i in opponent_list: 
        print(i.playernumber," - ",i.playername)  #prints opponents

    valid_choice = False  #setting up a big loop defined of two little loops, number check and name check
    while valid_choice == False:  #do this until good name or num return
        choice = input()

        if choice == 'exit':
            print("\nExiting PvP.")
            return

        if choice.isdigit():   #filters for input being a number
            if int(choice) not in op_player_nums:  # checks choice against valid player numbers
                print("Entered number not in range of valid choices, try again.")  # if not, throw an error
        else:
            if choice.lower() not in op_player_names:  # run choice against all possible opponent player names
                print("Invalid player name, try again.")  # if not, throw an error

        for i in opponent_list:   #look through opponent list
            if choice.isdigit():   #if player enters a number
                if int(choice) == int(i.playernumber):  #if num entry is a valid opponent number
                    opponent_player = i #sets opponent_player as the number you selected from list
                    valid_choice = True #sets flag to leave big loop
                    break   #leaves opponent list loop
            else:   #if not a digit, then name
                if choice.lower() == i.playername.lower():  #seeing if you typed the player name instead of player number
                    opponent_player = i #sets opponent_player as the name player typed from list
                    valid_choice = True  #sets flag to leave big loop
                    break #leaves opponent list loop

    print(f"You have selected {opponent_player.playername}.\n")

    ###chosing which of your opponents cards to curse###

    op_player_card_names = []   #bucket for opponent player card names
    op_player_card_nums = []   #same for card numbers based on list index

    for i in opponent_player.cardsinhand: op_player_card_names.append(i.name)   #filling op_player_card_names bucket
    op_player_card_names = [element.lower() for element in op_player_card_names]   #making cardnames lowercase

    for i in opponent_player.cardsinhand: op_player_card_nums.append(opponent_player.cardsinhand.index(i)) #filling op_player_card_nums bucket

    print(f"Select a card of {opponent_player.playername}'s to curse. Type name or number, or ('exit') to leave.")
    for i in opponent_player.cardsinhand: print(f"{opponent_player.cardsinhand.index(i)} - |{i.name}|")  #list's the selected player's hand

    valid_choice = False
    while valid_choice == False:
        choice = input()
        if choice == 'exit': return

        if choice.isdigit():
            if int(choice) not in op_player_card_nums:  # run choice against all possible opponent card nums
                print("Invalid Opponent Card number, try again.")  # if not, throw an error
        else:
            if choice.lower() not in op_player_card_names:
                print("Invalid Opponent Card name, try again.")

        for i in opponent_player.cardsinhand:
            if choice.isdigit():
                if int(choice) == int(opponent_player.cardsinhand.index(i)):
                    selected_card = i  # sets var selected_card based on cards in hand index number
                    valid_choice = True
                    break
            else:
                if choice.lower() == str(i.name.lower()):  #seeing if you typed the player name instead of player number
                    selected_card = i
                    valid_choice = True
                    break

        if len(selected_card.curse_bucket) > 0:   #only allows one curse per card
            print("Sorry, this card is already cursed. Try again on another selection.")
            return

    current_player.pvp_this_turn = True   #makes it so players can only use once per turn, resets on end sequence
    print(f"\nYou have cursed {opponent_player.playername}'s '{selected_card.name}' Boy card with {selected_pvp.type}.")
    long_delay()
    selected_pvp.used_on.append(opponent_player)  # copying opponent player to pvp card attribute bucket "used on"...might not be helpful
    selected_card.curse_bucket.append(selected_pvp) #adds selected PVP to the opponent's card curse bucket
    current_player.pvp_in_hand.remove(selected_pvp) #removes pvp card from current hand
    print("The spent PvP card has been removed from your hand.")
    long_delay()

def call_number(choice):
    if current_player.dialed_this_turn == False:
        valid_call = False   #initalizes valid call var
        for i in current_player.cardsinhand:   #this checks if dial "boyname" or dial "phonenum" was entered
            if "dial" in choice and str(i.phonenum) in choice or "dial" in choice and str(i.name).lower() in choice:
                last_dialed_boy = i
                for x in range(0, 3):
                    print("*ring*")
                    short_delay()
                return last_dialed_boy

        print("You pick up the phone to make a call. Please enter a number (or name).")  #get message if dial + nothing useful is entered

        while True:
            dialed_number=input()   #prompts a second input loop to get a valid person to call
            if dialed_number == "leave":
                break

            for i in current_player.cardsinhand:
                if dialed_number == i.phonenum or dialed_number.lower() == i.name.lower():   #added name dial for Clarissa <3
                    for x in range(0,3):
                        print("*ring*")
                        short_delay()
                    delay()
                    last_dialed_boy = i
                    valid_call = True

            if valid_call is True and len(player_list) > 1:
                return last_dialed_boy

            if valid_call is not True:
                print("Wrong number. Try another number or dial ('leave') to exit.")
    else: print("Cannot dial twice in a single turn.")

def clue_reveal(last_dialed_boy):
    try:
        last_dialed_boy
    except NameError:
        last_dialed_boy = None
    if last_dialed_boy == None: return
    #rejection check:
    if last_dialed_boy.clue_to_reveal == card_list[crush].hangout\
    or last_dialed_boy.clue_to_reveal == card_list[crush].sport\
    or last_dialed_boy.clue_to_reveal == card_list[crush].food\
    or last_dialed_boy.clue_to_reveal == card_list[crush].clothing: #if the clue would reveal the crush's hangout, food etc
        response = ClueType.NO_REVEAL                                    #we do not give that information to the player

    #type of reveal check:
    no_crush_list = copy.copy(card_list)   #we need to look through all clues except for the crush's 'positive' clues
    remove_it = card_list[crush]           # so I copy the master card list and remove the crush entry from it
    no_crush_list.remove(remove_it)
    for i in no_crush_list:   #iterate through the whole no crush list, checking against what kind of clue it is
        match last_dialed_boy.clue_to_reveal:       #and set the type of response
            case i.hangout:
                response = ClueType.HANGOUT
            case i.sport:
                response = ClueType.SPORT
            case i.food:
                response = ClueType.FOOD
            case i.clothing:
                response = ClueType.CLOTHING

#### player vs player effects when dialed ####

    curse_mod = check_for_curse(last_dialed_boy)

    if curse_mod == PvpCardType.HANG_UP:
        last_dialed_boy.curse_bucket.remove(last_dialed_boy.curse_bucket[0])   #deletes the curse from the game
        dialed_discard(last_dialed_boy)   #runs the discard script and skips clue reveal
        return #breaks out of current routine

    if last_dialed_boy.first_call:   #checks if this is your first time calling them
        print(blue_out(f"Hello? This is {last_dialed_boy.name}. You want to know about your crush?"))
        long_delay()
    else:   #if not first time, increase snark
        print(blue_out("You again? I already told you..."))
        long_delay()

    #loud repsonses, everyone hears
    print(blue_out(response.clue_text()))

    long_delay()

    #quiet response, only player hears

    clue_text = response.negative_clue_text(last_dialed_boy.clue_to_reveal)
    if (last_dialed_boy.clue_to_reveal == "Hat" or "Jacket" or "Tie") and (response == ClueType.CLOTHING): 
        clue_text = f"a {clue_text}"
    print(red_out(clue_text), "\n")

    current_player.collected_clues.append(last_dialed_boy)   #add clue to notepad

    if curse_mod == PvpCardType.SHARE_SECRET:
        also_give_clue = last_dialed_boy.curse_bucket[0].player_owner
        also_give_clue.collected_clues.append(last_dialed_boy) #player who used curse card gets clue
        current_player.pvp_in_hand.append(last_dialed_boy.curse_bucket[0])   #copy pvp card to whosturn
        last_dialed_boy.curse_bucket.remove(last_dialed_boy.curse_bucket[0])  #remove curse card from boy card
        for i in current_player.pvp_in_hand:
            i.player_owner = current_player   #brute force changes the owner flag of the pvp cards in who's turn hand
    
    elif curse_mod == PvpCardType.SPEAKERPHONE:
        for i in player_list:
            i.collected_clues.append(last_dialed_boy)   #give clue to all players in the game
        last_dialed_boy.curse_bucket.remove(last_dialed_boy.curse_bucket[0])   #delete the speakerphone card from the game

        #pvp card changes hand and owner assignment
    last_dialed_boy.first_call = False  #this is where redial snark is set

    choice = "null"
    long_delay()
    return choice

def dialed_discard(last_dialed_boy):
    if current_player.dialed_this_turn == False:
        i = current_player.cardsinhand.index(last_dialed_boy)
        print(f"{last_dialed_boy.name} from your hand has been discarded.")
        discard_pile.append(current_player.cardsinhand.pop(i))  # adds card to discard pile based on in_hand index num
        if len(player_list) > 1: current_player.dialed_this_turn = True

def dialed_draw():
    if len(current_player.cardsinhand) < 3:
        current_player.cardsinhand.append(game_deck.pop(0))
        print(current_player.playername, "drew a card.")
        choice = "null"
        return choice

def end_turn(number_of_players):
    global current_player
    print(f"Ending {current_player.playername}'s turn.")

    former_player = current_player  # Assign the current player as the fomer player
    if number_of_players > 1:
        for i in range(len(player_list)):   #iterates over all index numbers in player list var
            if player_list[i] == current_player:   #if i is the index number of the item matching current player:
                current_player_num = i  #sets var current_player_num to correct index number

        next_player_num = (current_player_num + 1) % len(player_list)
        current_player = player_list[next_player_num]
    
        delay()
        
        # End last player's turn
        former_player.end_turn()
        
        print("next player up:", current_player.playername)
        delay()

        for i in card_list:     #Reset redial flag when players swap
            i.first_call = True
        clear_screen()

def count():
    print(f"\n====Status====")
    short_delay()
    print(f"Draw Pile: {len(game_deck)}")
    short_delay()
    print(f"{current_player.playername}'s Hand: {len(current_player.cardsinhand)}")
    short_delay()
    print(f"Discard Pile: {len(discard_pile)}")
    short_delay()

def solve(crush, number_of_players):

    if current_player.guessed_this_turn:
        print("You cannot guess more than once per turn.")
        return False
    print("You think you know who your crush is, huh?\nType your guess to check (name or phone#).\nYou can also look at your notebook by entering ('notebook').")
    crush_object = card_list[crush]

    while True:
        solve_choice = input().lower()
        for i in card_list:
            if solve_choice == crush_object.phonenum or solve_choice == crush_object.name.lower():
                result = "crush"
                break
            if solve_choice == i.phonenum or solve_choice == i.name.lower():
                result = "valid"
                break
            else: result = "invalid"

        match result:
            case "invalid":
                print("invalid input. Try again.")
            case "crush":
                long_delay()
                print(f"{crush_object.name} is your crush!\n")
                print(f"Congratulations! {current_player.playername} (Player {current_player.playernumber}) has won the game.")
                long_delay()
                print("Game Over!")
                print("Thank you for playing! I hope you had fun. \n                                  - Old Kid")
                long_delay()
                long_delay()
                if number_of_players > 1: current_player.guessed_this_turn = True
                return True
            case "valid":
                print("Wrong boy, try again!")
                if number_of_players > 1: current_player.guessed_this_turn = True
                return False

def shuffle():  # shuffles the game deck
    random.shuffle(game_deck)
    print("\nCards in the game deck have been shuffled.")
    delay()

def reshuffle():
    if len(discard_pile) == 0: # check that discard pile is not empty
        print("There's nothing in the discard pile to shuffle back into the deck.")
    else:
        for i in range(len(discard_pile)): #does an i loop based on the number of items in the discard pile
            game_deck.append(discard_pile.pop(0)) #adds the discard pile back into the game deck
        random.shuffle(game_deck)
        print("\n",blue_out("The discard pile has been shuffled back to the draw pile."),"\n")

# now on to the main loop. it simply checks for inputs to run the outlined functions. nothing too crazy

def game_loop():
    global current_player

    clear_screen()
    crush = new_game_crush()
    valid_choices = ["null", "notepad", "dial", "end", "count", "redial", "solve", "pvp"] # commands that work at start
    print("\nWelcome to Dream Phone Simulator Version 0.1, a computer simulation of the 1991 board game 'Dreamphone'. \
          \nPlease see included dp_instructions.txt for more information.\n")
    delay()
    number_of_players = set_number_of_players()
    name_players()
    delay()
    current_player = starting_player()
    shuffle()
    starting_deal()

    game_ended = False

    while not game_ended:
        whos_turn(current_player)
        current_player.print_hand()
        short_delay()
        check_decks()
        print (white_out("Commands: ('dial') - ('notepad') - ('pvp') - ('solve') - ('redial') - ('end')"),"\n")
        choice = input().lower()

        if 'dial' in choice and choice != 'redial':
            last_dialed_boy = call_number(choice)
            clue_reveal(last_dialed_boy)
            dialed_discard(last_dialed_boy)
            dialed_draw()
            choice = "null"

        if choice not in valid_choices:
            print("Not a valid choice.")
        else:
            match choice:
                case 'solve':
                    game_ended = solve(crush, number_of_players)
                case 'count':
                    count()
                case 'pvp':
                    use_pvp()
                case 'redial':
                    try: last_dialed_boy
                    except NameError: last_dialed_boy = None
                    if last_dialed_boy == None: 
                        print("no call made yet")
                    else:
                        print(f"The last boy you called was {last_dialed_boy.name}. His number was {last_dialed_boy.phonenum}.")
                        clue_reveal(last_dialed_boy)
                case 'notepad':
                    boy_attribute_table()
                case 'end':
                    end_turn(number_of_players)

game_loop()