from typing import Dict

from nltk.sentiment.vader import SentimentIntensityAnalyzer


class NltkClassifier:
    """
    Classify entire strings with nltk's Vader API.
    """

    def __init__(self):
        self._analyser = SentimentIntensityAnalyzer()

    def analyse_text(self, txt: str) -> Dict[str, float]:
        """
        Analyse a text.
        :param txt: a string
        :return: A dictionary with 4 entries:
            'compound', 'neg', 'neu', 'pos'
        """
        return self._analyser.polarity_scores(txt)

    def is_negative(self, txt: str) -> bool:
        """
        Return True if the text is negative
        """
        res = self.analyse_text(txt)
        return res['compound'] < 0

    def is_positive(self, txt: str) -> bool:
        """
        Return True if the text is positive
        """
        res = self.analyse_text(txt)
        return res['compound'] > 0
