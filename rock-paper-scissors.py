from game import Game


def get_user_menu_choice():
    """
    Display menu and get user choice.
    """
    while True:
        print("\n--- ROCK PAPER SCISSORS ---")
        print("1. Play a new game")
        print("2. Show scores")
        print("3. Quit")

        choice = input("Choose an option: ")

        if choice in ["1", "2", "3"]:
            return choice
        else:
            print("Invalid choice. Please select 1, 2, or 3.")


def print_results(results):
    """
    Print the game results.
    """
    print("\nGame Results")
    print("Wins:", results["win"])
    print("Losses:", results["loss"])
    print("Draws:", results["draw"])
    print("\nThanks for playing!")


def main():
    results = {
        "win": 0,
        "loss": 0,
        "draw": 0
    }

    while True:
        choice = get_user_menu_choice()

        if choice == "1":
            game = Game()
            result = game.play()
            results[result] += 1

        elif choice == "2":
            print_results(results)

        elif choice == "3":
            print_results(results)
            break


if __name__ == "__main__":
    main()
