import random

SANTA_WELCOME_MESSAGES = [
    "Ho ho ho! 🎅 Welcome to the North Pole's chat room! I'm Santa Claus, ready to spread the magic of Christmas 🎄. What festive wonders can I assist you with today?",
    "Merry Christmas! 🌟 It's Santa here, bringing joy and cheer from the snowy North Pole ❄️. Tell me, what Christmas dreams can I help make come true for you today?",
    "Ho ho ho! 🎁 Santa Claus is in the house! I'm here to fill your day with Christmas magic and joy ✨. What jolly adventures shall we embark on today?",
    "Greetings from Santa's workshop! 🎄 It's the season of giving, and I'm here to give you a hearty welcome 🙌. What Christmas joy can Santa bring to you today?",
    "Hello, my festive friend! 🤗 Santa Claus is here to add sparkle to your Christmas 🌠. Let's chat about all things merry and bright. What can I do for you on this wonderful day?",
    "Ho ho ho! 🎉 Step into Santa's grotto, where every day is Christmas 🎅. How can I sprinkle some festive cheer on your day?",
    "Jingle bells, jingle bells, jingle all the way! 🔔 Oh, what fun it is to chat with Santa today! What Christmas wishes can I help come true?",
    "Warmest welcomes from the North Pole! ❄️ It's me, Santa, ready to share stories and joy 📖. What brings you to this jolly corner of the internet?",
    "Ho ho ho! 🎄 The spirit of Christmas is always here with Santa. Tell me, what festive tales or questions do you have for me today?",
    "Merry meet on this magical day! 🌈 Santa's here to share the joy and wonder of the holiday season 🌟. What Christmas magic can we create together?"
]


def get_santa_welcome_msg():
    return random.choice(SANTA_WELCOME_MESSAGES)
