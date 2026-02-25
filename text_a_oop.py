import string
import re
from collections import Counter


class Text:
    def __init__(self, text: str):
        self.text = text

    def word_frequency(self, word: str):
        words = self.text.lower().split()
        count = words.count(word.lower())
        return count if count > 0 else None

    def most_common_word(self):
        words = self.text.lower().split()
        freq = Counter(words)
        return freq.most_common(1)[0][0] if freq else None

    def unique_words(self):
        words = self.text.lower().split()
        return list(set(words))

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return cls(content)


# 🔹 Inheritance
class TextModification(Text):

    STOP_WORDS = {
        "a", "an", "the", "is", "are", "in", "on", "at", "to",
        "for", "of", "and", "or", "but", "this", "that", "it"
    }

    def remove_punctuation(self):
        cleaned = self.text.translate(str.maketrans("", "", string.punctuation))
        return cleaned

    def remove_stop_words(self):
        words = self.text.split()
        filtered = [w for w in words if w.lower() not in self.STOP_WORDS]
        return " ".join(filtered)

    def remove_special_characters(self):
        cleaned = re.sub(r"[^A-Za-z0-9\s]", "", self.text)
        return cleaned
