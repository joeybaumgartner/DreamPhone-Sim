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

class ClueType(Enum):
    HANGOUT = 1
    SPORT = 2
    FOOD = 3
    CLOTHING = 4

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