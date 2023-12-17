from enum import Enum

class PvpCardType(Enum):
    HANG_UP = 1
    SHARE_SECRET = 2
    SPEAKERPHONE = 3

    def __str__(self):
        match self:
            case PvpCardType.HANG_UP:
                return "Mom Says Hang up!"
            case PvpCardType.SHARE_SECRET:
                return "Share a Secret"
            case PvpCardType.SPEAKERPHONE:
                return "Speakerphone"
            
    def description(self):
        match self:
            case PvpCardType.HANG_UP:
                return "Mom Says Hang up!"
            case PvpCardType.SHARE_SECRET:
                return "Share a Secret"
            case PvpCardType.SPEAKERPHONE:
                return "Speakerphone"

class ClueType(Enum):
    HANGOUT = 1
    SPORT = 2
    FOOD = 3
    CLOTHING = 4
    NO_REVEAL = 5 

    def __str__(self):
        match self:
            case ClueType.HANGOUT:
                return "Hangout"
            case ClueType.SPORT:
                return "Sport"
            case ClueType.FOOD:
                return "Food"
            case ClueType.CLOTHING:
                return "Clothing"
            case ClueType.NO_REVEAL:
                return ""
            
    def clue_text(self):
        match self:
            case ClueType.HANGOUT:
                return "I know where he hangs out, "
            case ClueType.SPORT:
                return "He is very athletic, "
            case ClueType.FOOD:
                return "He eats a lot of food, "
            case ClueType.CLOTHING:
                return "He looks good in whatever he wears"
            
    def negative_clue_text(self, clue):
            match self:
                case ClueType.HANGOUT:
                    return f"but he doesn't hang out at {clue}."
                case ClueType.SPORT:
                    return f"but he doesn't like {clue}."
                case ClueType.FOOD:
                    return f"but he hates the taste of {clue}."
                case ClueType.CLOTHING:
                    return f"but he doesn't wear {clue}."