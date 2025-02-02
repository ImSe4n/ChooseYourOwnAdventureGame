"""
U6-A2 Adventure Game
ICS3U-01
Sean Nie
Description: A text-based adventure game where the player plays minigames to get keys and items to start the plane and escape.
2024-01-16: V1
"""

import time
import random

inventory = []
initial_cash = 10000
battery = 'not charged'

def colored_letter(letter, color):
    """
    Returns the colored letter based on the provided color.

    Args:
        letter (str): The letter to be colored.
        color (str): The color to use ('green', 'yellow', 'gray').

    Returns:
        str: The letter wrapped in ANSI color codes.
    """
    colors = {"green": "\033[92m", "yellow": "\033[93m",
              "gray": "\033[90m", "reset": "\033[0m"}
    result = f"{colors[color]}{letter}{colors['reset']}"
    return result

def reaction_game(delay, threshold):
    """
    Tests the player's reaction time.

    Args:
        delay (float): Seconds to wait before displaying "GO!".
        threshold (float): Maximum allowed reaction time in seconds.

    Returns:
        bool: True if the player's reaction time is within the threshold, False otherwise.
    """
    print("To start the GPU, I will test your reaction time.")
    print("When I say GO, hit ENTER as fast as you can.")
    time.sleep(1)
    print("Ready")
    time.sleep(1)
    print("Steady")
    time.sleep(delay)  # Use the provided delay
    print("GO!")
    tic = time.perf_counter()
    input()  # Wait for the player's response
    toc = time.perf_counter()
    time_spent = toc - tic
    print(f"Your reaction time: {time_spent:.2f} seconds.")
    result = (time_spent <= threshold)
    return result

def wordle(word_list=None, attempts=6):
    """
    Plays the Wordle minigame where the player guesses a 5-letter word.

    Args:
        word_list (list): List of valid words. If None, a default list is used.
        attempts (int): Number of attempts allowed.

    Returns:
        str: A location code indicating where to go next.
    """
    result = None
    if word_list is None:
        word_list = [
            "apple", "beach", "crane", "dance", "eagle", "fable", "giant", "honey", "igloo", "jolly",
            "karma", "lemon", "mango", "noble", "olive", "pearl", "quilt", "robin", "sugar", "tiger",
            "umbra", "vivid", "whale", "xenon", "yacht", "zebra", "abide", "blink", "crisp", "dwell",
            "elbow", "flame", "glide", "haste", "infer", "joust", "knack", "latch", "mirth", "nudge",
            "otter", "pluck", "quirk", "rival", "swoop", "tread", "usher", "vapor", "widen", "yearn",
            "abyss", "bluff", "chirp", "dodge", "ember", "froth", "grasp", "hover", "ivory", "jelly",
            "kiosk", "lurid", "mossy", "nymph", "opium", "pique", "quell", "rivet", "swirl", "tryst",
            "ultra", "viper", "waltz", "xylem", "yodel", "zesty", "amble", "brisk", "clasp", "drape",
            "evoke", "flint", "grime", "hitch", "inlay", "joust", "kayak", "lurch", "molar", "nudge",
            "oasis", "prank", "quash", "relic", "snipe", "tweak", "unzip", "vixen", "wryly", "zonal"
        ]
    secret_word = random.choice(word_list)
    print("Welcome to Wordle! Guess the 5-letter word.")
    for attempt in range(attempts):
        guess = input("Enter your guess: ").lower()
        while len(guess) != 5 or not guess.isalpha():
            print("Invalid guess. Please enter a 5-letter word.")
            guess = input("Enter your guess: ").lower()
        if guess == secret_word:
            print("\033[92mCongratulations! You guessed the word!\033[0m")
            inventory.append('atc_key')
            result = '2'
            break
        feedback = ""
        for i in range(5):
            if guess[i] == secret_word[i]:
                feedback += colored_letter(guess[i], "green")
            elif guess[i] in secret_word:
                feedback += colored_letter(guess[i], "yellow")
            else:
                feedback += colored_letter(guess[i], "gray")
        print(feedback)
    if result is None:
        print(f"Game over! The word was: {secret_word}. Please try again in 15 seconds.")
        time.sleep(15)
        result = security_checkpoint()
    return result

def hangman(words=None, attempts=6):
    """
    Plays the Hangman minigame where the player guesses letters of a word.

    Args:
        words (list): List of possible words. If None, a default list is used.
        attempts (int): Number of wrong attempts allowed.

    Returns:
        str: A location code indicating where to go next.
    """
    result = None
    if words is None:
        words = ["python", "programming", "hangman", "challenge", "developer", "algorithm"]
    word = random.choice(words)
    word_letters = set(word)
    guessed_letters = set()
    while attempts > 0 and word_letters:
        display_word = "".join([letter if letter in guessed_letters else "_" for letter in word])
        print(f"Word: {display_word}")
        print(f"Attempts left: {attempts}")
        print(f"Guessed letters: {', '.join(sorted(guessed_letters))}")
        guess = input("Guess a letter: ").lower()
        if len(guess) != 1:
            print("Please enter exactly one letter.")
            continue
        elif not guess.isalpha():
            print("Please enter a valid letter.")
            continue
        elif guess in guessed_letters:
            print("You already guessed that letter. Try again.")
            continue
        if guess in word_letters:
            print("Good guess!")
            guessed_letters.add(guess)
            word_letters.discard(guess)
        else:
            print("Wrong guess!")
            guessed_letters.add(guess)
            attempts -= 1
        print()
    if not word_letters:
        print(f"Congratulations! You guessed the word: {word}")
        inventory.append('h_key')
        result = '2'
    else:
        print(f"Game over! The word was: {word}. Please try again in 15 seconds.")
        time.sleep(15)
        result = office()
    return result

def tarmac():
    """
    Displays the tarmac location options.

    Returns:
        str: Next location code.
    """
    result = None
    print("You are on the tarmac. You are given a key to the terminal.")
    print("You can go to the terminal or stay here.")
    choice = input("Enter \n '1' to stay here \n '2' to go to the TERMINAL \n '3' to go to the FUEL TANK \n '4' to go to the ATC TOWER \n '5' to go to the HANGAR \n 'e' to quit the game \n > ")
    while choice not in ['1', '2', '3', '4', '5', 'e']:
        print("Invalid choice. Please enter a valid choice.")
        choice = input("Enter \n '1' to stay here \n '2' to go to the TERMINAL \n '3' to go to the FUEL TANK \n '4' to go to the ATC TOWER \n '5' to go to the HANGAR \n 'e' to quit the game \n > ")
    result = choice
    return result

def terminal(cash):
    """
    Displays the terminal location options.
    Args:
        cash (int): The player's current cash.
    Returns:
        str: Next location code.
    """
    result = None
    if 'atc_key' in inventory and 's_key' in inventory and cash >= 70000:
        print("You have all the keys and can go to the air traffic control tower and hangar. You can also buy fuel to start the plane.")
        result = '1'
    else:
        print("You are in the terminal. You can go to the lounge, ticket counter, or security checkpoint.")
        choice = input("Enter \n 'l' to go to the lounge \n 't' to go to the ticket counter \n 's' to go to the security checkpoint \n 'o' to go to the airline office \n '1' to return to the tarmac \n 'e' to quit the game \n > ")
        while choice not in ['l', 't', 's', 'o', '1', 'e']:
            print("Invalid choice. Please enter a valid choice.")
            choice = input("Enter \n 'l' to go to the lounge \n 't' to go to the ticket counter \n 's' to go to the security checkpoint \n 'o' to go to the airline office \n '1' to return to the tarmac \n 'e' to quit the game \n > ")
        result = choice
    return result

def lounge():
    """
    Lounge location where the player can play a minigame to obtain the security key.

    Returns:
        str: Next location code.
    """
    result = None
    if 's_key' in inventory:
        print("You have already visited the lounge and obtained the security room key.")
        result = '2'
    else:
        print("You are in the lounge. You see a security room key on the table.")
        print("You can play a minigame (guess the number) to get the key.")
        choice = input("Enter \n 'start' to begin the minigame \n '2' to go back to the terminal \n 'e' to quit the game \n > ")
        while choice not in ['start', '2', 'e']:
            print("Invalid choice. Please enter a valid choice.")
            choice = input("Enter \n 'start' to begin the minigame \n '2' to go back to the terminal \n 'e' to quit the game \n > ")
        if choice == 'start':
            print("You must guess the number from 1-50 to get the key. You will have 5 tries. I will tell you if the number is higher or lower.")
            tries = 5
            low = 1
            high = 50
            number = random.randint(low, high)
            while tries > 0:
                try:
                    guess = int(input("Enter your guess: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue
                while guess < low or guess > high:
                    print("Invalid input. Please enter a number between", low, "and", high, ".")
                    try:
                        guess = int(input("Enter your guess: "))
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                        continue
                if guess == number:
                    print("You got the key!")
                    inventory.append('s_key')
                    result = '2'
                    break
                elif guess < number:
                    print("Higher")
                else:
                    print("Lower")
                tries -= 1
            if result is None:
                print("You ran out of tries. Please restart the game in 15 seconds.")
                time.sleep(15)
                result = lounge()
        else:
            result = choice
    return result

def ticket_counter(cash):
    """
    This function is blackjack minigame where the player can earn cash to buy fuel.
    Args:
        cash (int): The player's current cash.
    Returns:
        int: The player's updated cash.
    """
    result = None
    if cash >= 70000:
        print("You have enough cash to buy fuel. You can go to the fuel station. - stop gambling >:(")
        result = '2'
    else:
        print("You are at the ticket counter. You can play a minigame to earn cash to buy fuel.")
        print("You can play blackjack against the computer to earn cash to buy fuel.")
        choice = input("Enter \n 'start' to play the minigame \n '2' to return to the main terminal \n 'e' to quit the game \n > ")
        while choice not in ['start', '2', 'e']:
            print("Invalid choice. Please enter a valid choice.")
            choice = input("Enter \n 'start' to play the minigame \n '2' to return to the main terminal \n 'e' to quit the game \n > ")
        if choice == 'start':
            print("You will play blackjack against the computer. You will start with $10000. Enter 'hit' or 'stand' to play.")
            cash = 10000
            while cash > 0:
                print("Your cash: $", cash)
                try:
                    bet = int(input("Enter your bet: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue
                while bet > cash or bet <= 0:
                    print("Invalid bet. Please enter a valid bet.")
                    try:
                        bet = int(input("Enter your bet: "))
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                        continue
                player_hand = random.randint(1, 11)
                computer_hand = random.randint(1, 11)
                print("Your hand: ", player_hand)
                cash -= bet
                player_choice = input("Enter 'hit' or 'stand': ")
                while player_choice not in ['hit', 'stand']:
                    print("Invalid choice. Please enter a valid choice.")
                    player_choice = input("Enter 'hit' or 'stand': ")
                while player_choice == 'hit':
                    player_hand += random.randint(1, 11)
                    print("Your hand: ", player_hand)
                    if player_hand > 21:
                        print("You busted! You lose.")
                        break
                    player_choice = input("Enter 'hit' or 'stand': ")
                if player_hand <= 21:
                    while computer_hand < 17:
                        computer_hand += random.randint(1, 11)
                    print("Computer's hand: ", computer_hand)
                    if computer_hand > 21 or player_hand > computer_hand:
                        print("You win!")
                        cash += bet * 2
                    else:
                        print("You lose.")
                if cash >= 70000:
                    print("You have enough cash to buy fuel. You can go to the fuel station. - stop gambling >:(")
                    result = '2'
                    break
            if cash < 70000 and result is None:
                print("You ran out of cash. Please try again in 15 seconds.")
                time.sleep(15)
                result = ticket_counter(cash)
        else:
            result = choice
    return result, cash

def security_checkpoint():
    """
    Security checkpoint where the player can play wordle to get the ATC key.

    Returns:
        str: Next location code.
    """
    result = None
    if 's_key' not in inventory:
        print("You don't have the key to the security checkpoint. Please go to the lounge to get the key.")
        result = '2'
    elif 'atc_key' in inventory:
        print("You have already visited the security checkpoint and obtained the ATC key.")
        result = '2'
    else:
        print("You are at the security checkpoint. You see keys on the table.")
        print("You can play wordle to get the key.")
        choice = input("Enter \n 'start' to begin the minigame \n '2' to go back to the main terminal \n 'e' to quit the game \n > ")
        while choice not in ['start', '2', 'e']:
            print("Invalid choice. Please enter a valid choice.")
            choice = input("Enter \n 'start' to begin the minigame \n '2' to go back to the main terminal \n 'e' to quit the game \n > ")
        if choice == 'start':
            result = wordle(None, 6)
        else:
            result = choice
    return result

def office():
    """
    Airline office where the player can play hangman to get the hangar key.

    Returns:
        str: Next location code.
    """
    result = None
    if 'h_key' in inventory:
        print("You have already visited the airline office and obtained the hangar key.")
        result = '2'
    else:
        print("You are at the airline office. You see the hangar key on the desk.")
        print("You can play hangman to get the key.")
        choice = input("Enter \n 'start' to begin the minigame \n '2' to go back to the main terminal \n 'e' to quit the game \n > ")
        while choice not in ['start', '2', 'e']:
            print("Invalid choice. Please enter a valid choice.")
            choice = input("Enter \n 'start' to begin the minigame \n '2' to go back to the main terminal \n 'e' to quit the game \n > ")
        if choice == 'start':
            result = hangman(None, 6)
        else:
            result = choice
    return result

def air_traffic_control_tower():
    """
    Air traffic control tower where the player can pick up items.

    Returns:
        str: Next location code.
    """
    result = None
    if 'atc_key' not in inventory:
        print("You need the air traffic control key to enter the air traffic control tower.")
        result = '1'
    elif 'blackbox' in inventory and 'radio' in inventory and 'battery' in inventory:
        print("You have already visited the air traffic control tower and obtained the items.")
        result = '1'
    else:
        print("You are in the air traffic control tower. You see a blackbox, battery and radio on the table.")
        print("You can pick these items up or leave.")
        choice = input("Enter '7' to get the items: ")
        if choice == '7':
            inventory.extend(['blackbox', 'radio', 'battery'])
            print("You have obtained the blackbox, radio and battery.")
            result = '5'
        else:
            result = '5'
    return result

def hangar():
    """
    Hangar location where the player can get the GPU, staircase, or enter the plane.

    Returns:
        str: Next location code.
    """
    result = None
    if 'h_key' not in inventory:
        print("You need the hangar key to enter the hangar.")
        result = '1'
    else:
        print("You are in the hangar. You see a GPU, staircase, and the plane.")
        choice = input("Enter: \n 'g' to get the GPU \n 's' to get the staircase \n 'p' to enter the plane \n > ")
        if choice == 'g':
            if 'gpu' in inventory:
                print("You have already obtained the GPU.")
                result = '5'
            elif 'battery' not in inventory:
                print("You need a battery to start the GPU.")
                result = '5'
            else:
                print("You have a battery to start the GPU.")
                delay = random.uniform(2, 5)
                if reaction_game(delay, 0.28):
                    print("You started the GPU in record time! You are a genius!")
                    inventory.append('gpu')
                    result = '5'
                else:
                    print("Your reaction was too slow. Try again.")
                    result = hangar()
        elif choice == 's':
            if 'staircase' in inventory:
                print("You have already obtained the staircase.")
                result = '5'
            else:
                print("You have obtained the staircase.")
                inventory.append('staircase')
                result = '5'
        elif choice == 'p':
            required = {'gpu', 'staircase', 'blackbox', 'radio', 'fuel'}
            if required.issubset(set(inventory)):
                print("You have all the items to start the plane.")
                result = plane()
            else:
                print("You do not have all the items to start the plane. You need the GPU, staircase, blackbox, fuel, and radio. Please go back and get the items.")
                result = '5'
        else:
            result = choice
    return result

def fuel_station(cash):
    """
    Fuel station where the player can buy fuel.
    Args:
        cash (int): The player's current cash.
    Returns:
        str: Next location code.
        int: Updated cash amount.
    """
    result = None
    if 'fuel' in inventory:
        print("You have already bought fuel.")
        result = '1'
    else:
        print("You are at the fuel station. You can buy fuel to start the plane.")
        choice = input("Enter \n 'buy' to buy fuel \n '1' to go back to the tarmac \n 'e' to quit the game \n >  ")
        while choice not in ['buy', '1', 'e']:
            choice = input("Invalid choice. Please enter \n 'buy' to buy fuel \n '1' to go back to the tarmac \n 'e' to quit the game \n >  ")
        if choice == 'buy':
            if cash < 70000:
                print("You do not have enough cash to buy fuel. Please go back to the ticket counter to earn more cash.")
                result = fuel_station(cash)
            else:
                print("You have bought fuel for $70000. You can start the plane.")
                cash -= 70000
                inventory.append('fuel')
                result = '1'
        else:
            result = choice
    return result, cash

def plane():
    """
    Plane location where the player must start the plane to win the game.

    Returns:
        str: 'e' to quit the game (win condition).
    """
    result = None
    print("You are at the plane. All you need to do is start the plane to win the game.")
    choice = input("Enter 'start' to win the game! \n > ")
    while choice != 'start':
        choice = input("Invalid choice. Please enter 'start' to win the game! \n > ")
    if choice == 'start':
        print("Congratulations! You have started the plane and escaped the airport. You win!")
        result = 'e'
    else:
        result = choice
    return result

def main():
    """Main function that directs the game flow."""
    print("Welcome to FlyFlyFly! You are at the airport and need to start the plane to escape.")
    cash = initial_cash
    choice = '1'
    while choice != 'e':
        if choice == '1':
            choice = tarmac()
        elif choice == '2':
            choice = terminal(cash)
        elif choice == '3':
             choice = fuel_station(cash)
        elif choice == '4':
            choice = air_traffic_control_tower()
        elif choice == '5':
            choice = hangar()
        elif choice == 's':
            choice = security_checkpoint()
        elif choice == 't':
            choice = ticket_counter(cash)
        elif choice == 'l':
            choice = lounge()
        elif choice == 'o':
            choice = office()
        elif choice == 'p':
            choice = plane()
        else:
            print("Invalid location code. Returning to the tarmac.")
            choice = '1'
    print("Thanks for playing!")

# Call the main function to start the game.
main()