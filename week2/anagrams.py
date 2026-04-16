from anagram_checker import AnagramChecker


def main():
    checker = AnagramChecker("words.txt")

    while True:
        print("\n--- ANAGRAM CHECKER ---")
        print("1. Enter a word")
        print("2. Exit")

        choice = input("Choose an option: ")

        if choice == "2":
            print("Goodbye!")
            break

        elif choice == "1":
            user_input = input("Enter a word: ").strip()

            # validation
            if len(user_input.split()) != 1:
                print("Error: Please enter only ONE word.")
                continue

            if not user_input.isalpha():
                print("Error: Only alphabetic characters are allowed.")
                continue

            word = user_input.lower()

            is_valid = checker.is_valid_word(word)
            anagrams = checker.get_anagrams(word)

            print("\nYOUR WORD:", word.upper())

            if is_valid:
                print("This is a valid English word.")
            else:
                print("This is NOT a valid English word.")

            if anagrams:
                print("Anagrams for your word:", ", ".join(anagrams))
            else:
                print("No anagrams found.")

        else:
            print("Invalid option. Please choose 1 or 2.")


if __name__ == "__main__":
    main()
