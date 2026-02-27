import random
from datetime import datetime

QUOTES = [
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("It always seems impossible until it's done.", "Nelson Mandela"),
    ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
    ("The future depends on what you do today.", "Mahatma Gandhi"),
    ("You don't have to be great to start, but you have to start to be great.", "Zig Ziglar"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("Success is not final, failure is not fatal.", "Winston Churchill"),
    ("Hard work beats talent when talent doesn't work hard.", "Tim Notke"),
    ("Your time is limited, don't waste it living someone else's life.", "Steve Jobs"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Dream big and dare to fail.", "Norman Vaughan"),
    ("Act as if what you do makes a difference. It does.", "William James"),
    ("Life is what happens when you're busy making other plans.", "John Lennon"),
    ("Spread love everywhere you go.", "Mother Teresa"),
    ("When you reach the end of your rope, tie a knot and hang on.", "Franklin D. Roosevelt"),
    ("Always remember that you are absolutely unique.", "Margaret Mead"),
    ("Do not go where the path may lead, go instead where there is no path.", "Ralph Waldo Emerson"),
    ("You will face many defeats in life, but never let yourself be defeated.", "Maya Angelou"),
    ("The greatest glory in living lies not in never falling, but in rising every time we fall.", "Nelson Mandela"),
    ("In the end, it's not the years in your life that count. It's the life in your years.", "Abraham Lincoln"),
    ("Never let the fear of striking out keep you from playing the game.", "Babe Ruth"),
    ("Life is either a daring adventure or nothing at all.", "Helen Keller"),
    ("Many of life's failures are people who did not realize how close they were to success.", "Thomas A. Edison"),
    ("You have brains in your head. You have feet in your shoes.", "Dr. Seuss"),
    ("If life were predictable it would cease to be life.", "Eleanor Roosevelt"),
]

def get_quote_of_the_day():
    """Returns a random quote every time app opens."""
    return random.choice(QUOTES)

def get_random_quote():
    return random.choice(QUOTES)