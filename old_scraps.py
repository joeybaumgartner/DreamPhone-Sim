#boy_attribute_table()

# I need to figure out how I want to do loud / quiet stuff with the text parser - might not be possible? focus on single player? / make pico dreamphone? I think i should
# at least program the effect -"this part is quiet", "this part is loud" to practice the logic before i get sound involved. need to take recordings of dreamphone repsonses - maybe move project
# to a website to act as phone (use a cellphone) and use real feelie cards /etc... i dunno hitting a logistical wall

###moving outdated functions down here###
#the following stuff is just to give some text feedback in the test program, not too interesting.
def call_number(choice):
    valid_call = ()   #initalizes valid call var
    for i in whos_turn().cardsinhand:   #this checks if dial "boyname" or dial "phonenum" was entered
        if "dial" in choice and str(i.phonenum) in choice or "dial" in choice and str(i.name).lower() in choice:
            last_dialed_boy = i
            return last_dialed_boy

    print("You pick up the phone to make a call. Please enter a number (or name).")  #get message if dial + nothing useful is entered

    while True:
        dialed_number=input()   #prompts a second input loop to get a valid person to call
        if dialed_number == "leave":
            break

        for i in whos_turn().cardsinhand:
            if dialed_number == i.phonenum or dialed_number.lower() == i.name.lower():   #added name dial for Clarissa <3
                for x in range(0,3):
                    print("ring")
                    short_delay()
                delay()
                last_dialed_boy = i
                valid_call = True

        if valid_call is True:
            return last_dialed_boy

        if valid_call is not True:
            print("Wrong number. Try another number or dial ('leave') to exit.")

def look():
    if len(whos_turn().cardsinhand) == 0:
        print("There are no cards in your hand.\n")
    else:
        print(whos_turn().playername,"looks closely at the cards in their hand.")
        for i in whos_turn().cardsinhand:
            print(str(i.name),"- Phone#:",(i.phonenum))
            short_delay()
    delay
def show_deck():
    if len(game_deck) == 0:
        print ("There are no cards in the draw deck.\n")
    else:
        print("The cards in the deck are:")
        for i in game_deck: print(i.name)
def count_deck():
    if len(game_deck) == 0:
        print ("There are no cards in the draw deck.\n")
    else:
        print("The number of cards in the draw deck are:", len(game_deck))
def show_hand():
    if len(whos_turn().cardsinhand) == 0:
        print("There are no cards in your hand.\n")
    else:
        print("Cards in", whos_turn().playername, "'s hand are:")
        for i in whos_turn().cardsinhand:
            print (i.name)
            short_delay()
    for i in whos_turn().collected_clues:
        print ("clues you got:", i.name)
def show_discard():
    if len(discard_pile) == 0:
        print ("There are no cards in the discard pile.\n")
    else:
        print("The cards in the discard pile are:")
        for i in discard_pile: print(i.name)
def count_hand():
    if len(whos_turn().cardsinhand) == 0:
        print ("There are no cards in your hand.\n")
    else:
        print("number of cards in your hand are:", len(whos_turn().cardsinhand))
def count_discard():
    if len(discard_pile) == 0:
        print ("There are no cards in the discard pile.\n")
        delay()
    else:
        print("number of cards in the discard pile:", len(discard_pile))
        delay()
def discard_choice():
    loop = 1
    while loop == 1:
        if len(whos_turn().cardsinhand) == 0:  # check that your hand is not empty
            print("you have no cards to discard.")
            delay()
            break
        else:
            show_hand()
            print("Please choose the card you wish to discard, or type 'back' to leave.")
            card_choice = input().lower() #which card do you want to discard?
            if card_choice == 'back': #gives a way to back out of the discard choice loop
                print("Exiting discard choice...")
                break #leaves discard choice loop
            else:
                for i in range(len(whos_turn().cardsinhand)):  #runs through the list count of in_hand
                    if card_choice == (whos_turn().cardsinhand[i].name.lower()): #checks if choice is in your hand
                        print(whos_turn().cardsinhand[i].name,"from your hand has been discarded.")
                        discard_pile.append(whos_turn().cardsinhand.pop(i)) #adds card to discard pile based on in_hand index num
                        loop = 0
                        delay()
                        break
                else: #if not 0 cards and if not a in_hand[i].name, incorrect choice
                    print ("Incorrect choice.")
def draw(num_count):  # function to move cards from the game deck into your hand
    if len(game_deck) == 0: #checks for an empty draw deck and displays an error if you draw from it
        print("Cannot draw any cards, the deck is empty.\n")
    else:
        if int(len(game_deck)) < num_count: #checks that you aren't trying to draw more cards than exist in the deck
            print("You can't draw more cards than the deck contains.\n")
        else:
            print(whos_turn().playername, "drew", num_count, "cards.")
            for i in range(num_count):  # I counts the number of draw_count specified
                whos_turn().cardsinhand.append(game_deck.pop(0))
    show_hand()
def discard(num_count):
    if len(whos_turn().cardsinhand) == 0:  # check that your hand is not empty
        print("you have no cards to discard.")
        delay()
    else:
        if int(len(whos_turn().cardsinhand)) < num_count: #checks that you aren't trying to discard more cards than are in your hand
            print("You cannot discard more cards than you have in hand.")
        else:
            print("You are discarding", num_count, "cards.")
            for i in range(num_count):  # i counts the number of discard_count specified
                discard_pile.append(whos_turn().cardsinhand.pop(i)) #moves in hand card to discard pile
def ask_for_num():
    print("Type 'back' or '0' to leave.")
    while True: #starts the loop
        i = input() #asks for player input
        if i: #this is a trick to validate against null entires (accidentally hitting enter)
            if i == 'back': #gives a way out
                print("No cards selected.")
                return i #returns i to the main program as 'back'
            if i.isdigit() == True: #checks if the user input is a number
                if i == 0: #checks for 0 entry
                    print("No cards selected.")
                else:
                    return int(i)  # returns either valid number or 0
            if i.isdigit() == False:
                print("Incorrect entry. Please enter a number, or type 'back' or '0' to leave.")

        else: #if not i, then print error instead of passing junk
            print("Incorrect entry. Please enter a number, or type 'back' or '0' to leave.")

#scraps

#            if choice == 'discard':
#                print("how many cards would you like to discard?")
#                num_count = ask_for_num()
#                if num_count == 'back' or num_count == '0':
#                    continue
#                else:
#                    discard(num_count)

#            if choice == 'discard choice':
#                discard_choice()

#            if choice == 'reshuffle': reshuffle()
#            if choice == 'shuffle': shuffle()
#            if choice == 'count deck': count_deck()
#            if choice == 'count hand': count_hand()
#            if choice == 'count discard': count_discard()
#            if choice == 'show deck': show_deck()
#            if choice == 'show hand': show_hand()
#            if choice == 'show discard': show_discard()
            if choice == 'more':
                print("More commands: ('shuffle') - ('draw') - ('discard') - ('end') - ('discard choice') - ('reshuffle') - You can type 'show' or 'count' to show or count your hand, draw pile and discard pile. Using 'show' or 'count' plus 'hand', 'deck' or 'discard' will display or count the individual respective stacks.")

            if choice == 'look': look()

            if choice == 'draw':
                print("how many cards would you like to draw?")
                num_count = ask_for_num()
                if num_count == "back" or 0:
                    continue
                else:
                    draw(num_count)