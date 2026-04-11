import random


class Game:

    def get_user_item(self):
        """
        Ask the user to choose rock, paper or scissors.
        Validate the input.
        """
        while True:
            choice = input("Choose rock, paper, or scissors: ").lower().strip()

            if choice in ["rock", "paper", "scissors"]:
                return choice
            else:
                print("Invalid choice. Please choose rock, paper, or scissors.")

    def get_computer_item(self):
        """
        Randomly select rock, paper, or scissors for the computer.
        """
        return random.choice(["rock", "paper", "scissors"])

    def get_game_result(self, user_item, computer_item):
        """
        Determine the result of the game.
        Returns: win, loss, or draw
        """
        if user_item == computer_item:
            return "draw"

        if (
            (user_item == "rock" and computer_item == "scissors") or
            (user_item == "paper" and computer_item == "rock") or
            (user_item == "scissors" and computer_item == "paper")
        ):
            return "win"

        return "loss"

    def play(self):
        """
        Play one round of the game.
        """
        user_item = self.get_user_item()
        computer_item = self.get_computer_item()

        result = self.get_game_result(user_item, computer_item)

        print("\nYou chose:", user_item)
        print("Computer chose:", computer_item)
        print("Result:", result)

        return result
