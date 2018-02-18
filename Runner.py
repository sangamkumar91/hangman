from Hangman import Hangman


def main():
    hangman = Hangman()
    while True:
        won, state = hangman.begin()
        if won:
            print("Won! The string is: " + state)
        else:
            print("Could not win. Starting again")
        hangman = Hangman()


if __name__ == "__main__":
    main()