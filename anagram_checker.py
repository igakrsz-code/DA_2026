class AnagramChecker:
    def __init__(self, word_list_file):
        """
        Load words from a text file into a set for fast searching.
        """
        with open(word_list_file, "r") as file:
            self.word_list = set(word.strip().lower() for word in file)

    def is_valid_word(self, word):
        """
        Check if a word exists in the word list.
        """
        return word.lower() in self.word_list

    def is_anagram(self, word1, word2):
        """
        Check if two words are anagrams.
        """
        return sorted(word1.lower()) == sorted(word2.lower())

    def get_anagrams(self, word):
        """
        Return a list of anagrams for the given word.
        """
        word = word.lower()
        anagrams = []

        for candidate in self.word_list:
            if candidate != word and self.is_anagram(word, candidate):
                anagrams.append(candidate)

        return anagrams
