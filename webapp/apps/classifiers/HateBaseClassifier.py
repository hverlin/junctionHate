import pandas as pd
import re


class HateBaseClassifier:
    """
    Allows to classifiy given strings by appereance in the hatebase data.
    """

    def __init__(self):
        import os
        cwd = os.getcwd()
        print(cwd)
        self.hatebase = pd.read_json("apps/data/hatebase/vocabulary.json")

    def classify(self, message):
        """
        Classify every word in given message as hate or not

        :param message:
        :return: list of booleans for every word
        """
        try:
            return list(map(self.is_hate_word, message.split()))
        except Exception:
            print("Error with message" + message)

    def is_hate_word(self, word):
        """
        Check if word is contained in hatebase data.
        :param word:
        :return: boolean
        """
        reg_w = "^{0};|^{0}$".format(re.escape(word))
        return len(self.hatebase[(self.hatebase["variants"].str.match(reg_w, na=False)) |
                                 (self.hatebase["vocabulary"] == word)]) > 0
