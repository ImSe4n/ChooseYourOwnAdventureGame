"""
U6-A2 Adventure Game
ICS3U-01
Sean Nie
Description: A text-based adventure game where the player plays minigames to get keys and items to start the plane and escape.
2024-01-16: V1
"""

import time
import random

# Global variables for inventory, initial cash, and battery status.
inventory = []
initial_cash = 10000
battery = 'not charged'

# ----------------------------------------------------------------------
# colored_letter: Returns a letter wrapped in ANSI color codes.
# ----------------------------------------------------------------------
def colored_letter(letter, color):
    """
    Returns the colored letter based on the provided color.

    Args:
        letter (str): The letter to be colored.
        color (str): The color to use ('green', 'yellow', 'gray').

    Returns:
        str: The letter wrapped in ANSI color codes.
    """
    # Define the ANSI codes for each color.
    colors = {"green": "\033[92m", "yellow": "\033[93m",
              "gray": "\033[90m", "reset": "\033[0m"}
    result = f"{colors[color]}{letter}{colors['reset']}"
    return result

# ----------------------------------------------------------------------
# reaction_game: Tests the player's reaction time.
# ----------------------------------------------------------------------
def reaction_game(delay, threshold):
    """
    Tests the player's reaction time.

    Args:
        delay (float): Seconds to wait before displaying "GO!".
        threshold (float): Maximum allowed reaction time in seconds.

    Returns:
        bool: True if the player's reaction time is within the threshold, False otherwise.
    """
    # Inform the player and add pauses for dramatic effect.
    print("To start the GPU, I will test your reaction time.")
    print("When I say GO, hit ENTER as fast as you can.")
    time.sleep(1)
    print("Ready")
    time.sleep(1)
    print("Steady")
    # Wait for the specified delay
    time.sleep(delay)
    print("GO!")
    # Start timing immediately after "GO!" is displayed.
    tic = time.perf_counter()
    #Wait for the player's reaction
    input()
    toc = time.perf_counter()
    time_spent = toc - tic
    print(f"Your reaction time: {time_spent:.2f} seconds.")
    result = (time_spent <= threshold)
    return result

# ----------------------------------------------------------------------
# wordle: Implements the Wordle minigame.
# ----------------------------------------------------------------------
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
    # Use default word list if none provided.
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
    
    # Loop through the allowed number of attempts.
    for attempt in range(attempts):
        guess = input("Enter your guess: ").lower()
        # Validate the guess is a 5-letter alphabetic string.
        while len(guess) != 5 or not guess.isalpha():
            print("Invalid guess. Please enter a 5-letter word.")
            guess = input("Enter your guess: ").lower()
        # Check for a correct guess.
        if guess == secret_word:
            print("\033[92mCongratulations! You guessed the word!\033[0m")
            inventory.append('atc_key')
            result = '2'
            break
        # Build and print feedback with colored letters.
        feedback = ""
        for i in range(5):
            if guess[i] == secret_word[i]:
                feedback += colored_letter(guess[i], "green")
            elif guess[i] in secret_word:
                feedback += colored_letter(guess[i], "yellow")
            else:
                feedback += colored_letter(guess[i], "gray")
        print(feedback)
    
    # If the word wasn't guessed, pause and return the player to the security checkpoint.
    if result is None:
        print(f"Game over! The word was: {secret_word}. Please try again in 15 seconds.")
        time.sleep(15)
        result = security_checkpoint()
    return result

# ----------------------------------------------------------------------
# hangman: Implements the Hangman minigame.
# ----------------------------------------------------------------------
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
    # Use default list if none is provided.
    if words is None:
        words = ["python", "programming", "hangman", "challenge", "developer", "algorithm"]
    word = random.choice(words)
    word_letters = set(word)  # Letters that must be guessed.
    guessed_letters = set()   # Letters already guessed by the player.
    
    # Loop until all letters are guessed or attempts run out.
    while attempts > 0 and word_letters:
        display_word = "".join([letter if letter in guessed_letters else "_" for letter in word])
        print(f"Word: {display_word}")
        print(f"Attempts left: {attempts}")
        print(f"Guessed letters: {', '.join(sorted(guessed_letters))}")
        guess = input("Guess a letter: ").lower()
        # Validate the guess.
        if len(guess) != 1:
            print("Please enter exactly one letter.")
            continue
        elif not guess.isalpha():
            print("Please enter a valid letter.")
            continue
        elif guess in guessed_letters:
            print("You already guessed that letter. Try again.")
            continue
        # Process the guess.
        if guess in word_letters:
            print("Good guess!")
            guessed_letters.add(guess)
            word_letters.discard(guess)
        else:
            print("Wrong guess!")
            guessed_letters.add(guess)
            attempts -= 1
        print()
    
    # Determine if the player has won or lost.
    if not word_letters:
        print(f"Congratulations! You guessed the word: {word}")
        inventory.append('h_key')
        result = '2'
    else:
        print(f"Game over! The word was: {word}. Please try again in 15 seconds.")
        time.sleep(15)
        result = office()
    return result

# ----------------------------------------------------------------------
# tarmac: Presents the tarmac location options.
# ----------------------------------------------------------------------
def tarmac():
    """
    Displays the tarmac location options.

    Returns:
        str: Next location code.
    """
    result = None
    print("You are on the tarmac. You are given a key to the terminal.")
    print("You can go to the terminal or stay here.")
    # Prompt the player for their choice.
    choice = input("Enter \n '1' to stay here \n '2' to go to the TERMINAL \n '3' to go to the FUEL TANK \n '4' to go to the ATC TOWER \n '5' to go to the HANGAR \n 'e' to quit the game \n > ")
    # Validate the input.
    while choice not in ['1', '2', '3', '4', '5', 'e']:
        print("Invalid choice. Please enter a valid choice.")
        choice = input("Enter \n '1' to stay here \n '2' to go to the TERMINAL \n '3' to go to the FUEL TANK \n '4' to go to the ATC TOWER \n '5' to go to the HANGAR \n 'e' to quit the game \n > ")
    result = choice
    return result

# ----------------------------------------------------------------------
# terminal: Presents the terminal location options.
# ----------------------------------------------------------------------
def terminal(cash):
    """
    Displays the terminal location options.
    
    Args:
        cash (int): The player's current cash.
        
    Returns:
        str: Next location code.
    """
    result = None
    # If the player has all keys and enough cash, allow direct access.
    if 'atc_key' in inventory and 's_key' in inventory and cash >= 70000:
        print("You have all the keys and can go to the air traffic control tower and hangar. You can also buy fuel to start the plane.")
        result = '1'
    else:
        print("You are in the terminal. You can go to the lounge, ticket counter, or security checkpoint.")
        # Prompt the player for their next destination.
        choice = input("Enter \n 'l' to go to the lounge \n 't' to go to the ticket counter \n 's' to go to the security checkpoint \n 'o' to go to the airline office \n '1' to return to the tarmac \n 'e' to quit the game \n > ")
        while choice not in ['l', 't', 's', 'o', '1', 'e']:
            print("Invalid choice. Please enter a valid choice.")
            choice = input("Enter \n 'l' to go to the lounge \n 't' to go to the ticket counter \n 's' to go to the security checkpoint \n 'o' to go to the airline office \n '1' to return to the tarmac \n 'e' to quit the game \n > ")
        result = choice
    return result

# ----------------------------------------------------------------------
# lounge: Allows the player to play a minigame to get the security key.
# ----------------------------------------------------------------------
def lounge():
    """
    Lounge location where the player can play a minigame to obtain the security key.

    Returns:
        str: Next location code.
    """
    result = None
    # Check if the security key has already been acquired.
    if 's_key' in inventory:
        print("You have already visited the lounge and obtained the security room key.")
        result = '2'
    else:
        print("You are in the lounge. You see a security room key on the table.")
        print("You can play a minigame (guess the number) to get the key.")
        # Prompt for starting the minigame or returning.
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
            # Loop through the allowed number of tries.
            while tries > 0:
                try:
                    guess = int(input("Enter your guess: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue
                # Validate the guess is within range.
                while guess < low or guess > high:
                    print("Invalid input. Please enter a number between", low, "and", high, ".")
                    try:
                        guess = int(input("Enter your guess: "))
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                        continue
                # Check if the guess is correct.
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
            # If no correct guess, restart the lounge minigame after a pause.
            if result is None:
                print("You ran out of tries. Please restart the game in 15 seconds.")
                time.sleep(15)
                result = lounge()
        else:
            result = choice
    return result

# ----------------------------------------------------------------------
# ticket_counter: Blackjack minigame to earn cash.
# ----------------------------------------------------------------------
def ticket_counter(cash):
    """
    This function is a blackjack minigame where the player can earn cash to buy fuel.
    
    Args:
        cash (int): The player's current cash.
        
    Returns:
        int: The player's updated cash.
        str: The next location code.
    """
    result = None
    # If the player already has enough cash, direct them to the fuel station.
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
           # Reset cash for the blackjack minigame.
            cash = 10000
            # Continue rounds until cash is sufficient or runs out.
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
                cash -= bet  # Deduct the bet from cash.
                player_choice = input("Enter 'hit' or 'stand': ")
                while player_choice not in ['hit', 'stand']:
                    print("Invalid choice. Please enter a valid choice.")
                    player_choice = input("Enter 'hit' or 'stand': ")
                # Allow player to hit until they stand or bust.
                while player_choice == 'hit':
                    player_hand += random.randint(1, 11)
                    print("Your hand: ", player_hand)
                    if player_hand > 21:
                        print("You busted! You lose.")
                        break
                    player_choice = input("Enter 'hit' or 'stand': ")
                if player_hand <= 21:
                    # Dealer's turn: hit until hand is at least 17.
                    while computer_hand < 17:
                        computer_hand += random.randint(1, 11)
                    print("Computer's hand: ", computer_hand)
                    if computer_hand > 21 or player_hand > computer_hand:
                        print("You win!")
                        # Player wins double the bet.
                        cash += bet * 2
                    else:
                        print("You lose.")
                # Check if cash is sufficient to stop gambling.
                if cash >= 70000:
                    print("You have enough cash to buy fuel. You can go to the fuel station. - stop gambling >:(")
                    result = '2'
                    break
            if cash < 70000 and result is None:
                print("You ran out of cash. Please try again in 15 seconds.")
                time.sleep(15)
                result = ticket_counter(cash)[0]
        else:
            result = choice
    return result, cash

# ----------------------------------------------------------------------
# security_checkpoint: Allows player to play Wordle to get the ATC key.
# ----------------------------------------------------------------------
def security_checkpoint():
    """
    Security checkpoint where the player can play wordle to get the ATC key.

    Returns:
        str: Next location code.
    """
    result = None
    # If the security key is missing, direct the player to the lounge.
    if 's_key' not in inventory:
        print("You don't have the key to the security checkpoint. Please go to the lounge to get the key.")
        result = '2'
    # If the ATC key is already obtained, no need to play again.
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

# ----------------------------------------------------------------------
# office: Allows player to play Hangman to get the hangar key.
# ----------------------------------------------------------------------
def office():
    """
    Airline office where the player can play hangman to get the hangar key.

    Returns:
        str: Next location code.
    """
    result = None
    # If the hangar key is already in inventory, notify the player.
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

# ----------------------------------------------------------------------
# air_traffic_control_tower: Allows player to pick up specific items.
# ----------------------------------------------------------------------
def air_traffic_control_tower():
    """
    Air traffic control tower where the player can pick up items.

    Returns:
        str: Next location code.
    """
    result = None
    # Check if the player has the necessary key.
    if 'atc_key' not in inventory:
        print("You need the air traffic control key to enter the air traffic control tower.")
        result = '1'
    # Check if items are already collected.
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

# ----------------------------------------------------------------------
# hangar: Allows player to obtain the GPU, staircase, or start the plane.
# ----------------------------------------------------------------------
def hangar():
    """
    Hangar location where the player can get the GPU, staircase, or enter the plane.

    Returns:
        str: Next location code.
    """
    result = None
    # Check if the hangar key is present.
    if 'h_key' not in inventory:
        print("You need the hangar key to enter the hangar.")
        result = '1'
    else:
        print("You are in the hangar. You see a GPU, staircase, and the plane.")
        choice = input("Enter: \n 'g' to get the GPU \n 's' to get the staircase \n 'p' to enter the plane \n > ")
        if choice == 'g':
            # Check for prerequisites before starting the GPU reaction test.
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
            # Check if the staircase is already collected.
            if 'staircase' in inventory:
                print("You have already obtained the staircase.")
                result = '5'
            else:
                print("You have obtained the staircase.")
                inventory.append('staircase')
                result = '5'
        elif choice == 'p':
            # Ensure the player has all required items before starting the plane.
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

# ----------------------------------------------------------------------
# fuel_station: Allows the player to buy fuel.
# ----------------------------------------------------------------------
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
    # If fuel has already been bought, notify the player.
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
                result = fuel_station(cash)[0]
            else:
                print("You have bought fuel for $70000. You can start the plane.")
                cash -= 70000
                inventory.append('fuel')
                result = '1'
        else:
            result = choice
    return result, cash

# ----------------------------------------------------------------------
# plane: Starts the plane, which ends the game.
# ----------------------------------------------------------------------
def plane():
    """
    Plane location where the player must start the plane to win the game.
    
    Returns:
        str: 'e' to quit the game (win condition).
    """
    result = None
    print("You are at the plane. All you need to do is start the plane to win the game.")
    # Loop until the player correctly inputs 'start'.
    choice = input("Enter 'start' to win the game! \n > ")
    while choice != 'start':
        choice = input("Invalid choice. Please enter 'start' to win the game! \n > ")
    if choice == 'start':
        print("Congratulations! You have started the plane and escaped the airport. You win!")
        result = 'e'
    else:
        result = choice
    return result

# ----------------------------------------------------------------------
# main: Directs the overall game flow.
# ----------------------------------------------------------------------
def main():
    """Main function that directs the game flow."""
    print("Welcome to FlyFlyFly! You are at the airport and need to start the plane to escape.")
    cash = initial_cash  # Local cash variable maintained in main
    choice = '1'
    # Main game loop continues until the player quits (choice == 'e').
    while choice != 'e':
        if choice == '1':
            choice = tarmac()
        elif choice == '2':
            choice = terminal(cash)
        elif choice == '3':
            choice, cash = fuel_station(cash)
        elif choice == '4':
            choice = air_traffic_control_tower()
        elif choice == '5':
            choice = hangar()
        elif choice == 's':
            choice = security_checkpoint()
        elif choice == 't':
            choice, cash = ticket_counter(cash)
        elif choice == 'l':
            choice = lounge()
        elif choice == 'o':
            choice = office()
        elif choice == 'p':
            choice = plane()
        else:
            # If an invalid code is encountered, default back to the tarmac.
            print("Invalid location code. Returning to the tarmac.")
            choice = '1'
    print("Thanks for playing!")

# ----------------------------------------------------------------------
# Start the game by calling main().
# ----------------------------------------------------------------------
main()
