import requests # To grab the page
from bs4 import BeautifulSoup   # To create the beuatifulsoup object
from csv import writer  # To read and write csv files
from time import sleep  # To and delays to the execution of the program
from random import choice   # To return a random element

# List to store all the quotes
all_quotes = []

# Contant portion of the url
base_url = "http://quotes.toscrape.com/"

# Variable portion of the url
url = "/page/1"

# Loop through all the pages in the website
while url:
    res = requests.get(f"{base_url}{url}")
    print(f"Now scraping {base_url}{url} ...")

    soup = BeautifulSoup(res.text, "html.parser")   # Create BeautifulSoup object

    quotes = soup.find_all(class_="quote")  # Extract all "quote" class objects

    # Extract information from each "quote" class object and store into all_quotes
    for quote in quotes:
        all_quotes.append({
            "text": quote.find(class_="text").get_text(),
            "author": quote.find(class_="author").get_text(),
            "bio-link": quote.find('a')["href"]
        })

    # Seach for the "Next" button
    next_btn = soup.find(class_="next")
    url = next_btn.find('a')["href"] if next_btn else None
    sleep(2)    # delay 2 seconds between each page

quote = choice(all_quotes)  # Pick a random quote
remaining_guesses = 4       # Initlise number of guesses
print("Here's a quote:")
print(f"{quote['text']}")
guess = ""  # Variable to hold user guess input

while guess.lower() != quote['text'].lower() and remaining_guesses > 0:
    guess = input(f"Who said this quote? Remaining guesses: {remaining_guesses}\n")

    # If user guesse correctly
    if guess.lower() == quote["author"].lower():
        print("Woo hoo! That's right!")
        break

    remaining_guesses -= 1
    print("That's not right.")

    # First try, provide hint on author's birthday and place
    if remaining_guesses == 3:
        # Scrape link with author's bio
        res = requests.get(f"{base_url}{quote['bio-link']}")
        soup = BeautifulSoup(res.text, 'html.parser')
        # Obtain birth date and birth place
        birth_date = soup.find(class_="author-born-date").get_text()
        birth_place = soup.find(class_="author-born-location").get_text()
        print(f"Here's a hint: The author was born on {birth_date} {birth_place}")

    # Second try, provide hint on first character of author's name
    if remaining_guesses == 2:
        print(f"Here's a hint: The author's name starts with the letter \'{quote['author'][0]}\'")

    # Last try, provide a hit on the last character of the author's name
    if remaining_guesses == 1:
        print(f"Here's a hint: The author's name ends with the letter \'{quote['author'][-1]}\'")

    if remaining_guesses == 0:
        print(f"The correct answer was \"{quote['author']}\"")
