import pandas as pd


class HateBaseClassifier:
    """
    Allows to classifiy given strings by appereance in the hatebase data.
    """

    def __init__(self):
        self.hatebase = pd.read_json("../data/hatebase/vocabulary.json")

    def classify(self, message):
        """
        Classify every word in given message as hate or not

        :param message:
        :return: list of booleans for every word
        """
        return list(map(self.is_hate_word, message.split()))

    def is_hate_word(self, word):
        """
        Check if word is contained in hatebase data.
        :param word:
        :return: boolean
        """
        reg_w = "^{0};|^{0}$".format(word)
        return len(self.hatebase[(self.hatebase["variants"].str.match(reg_w, na=False)) | (self.hatebase["vocabulary"] == word)]) > 0

