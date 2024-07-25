import unittest
from analyze_sentiment import analyze_sentiment

class TestAnalyzeSentiment(unittest.TestCase):
    def test_positive_sentiment(self):
        text = "Tesla to the moon!"
        sentiment = analyze_sentiment([text])
        self.assertGreater(sentiment['Tesla']['combined_sentiment'], 0)

    def test_negative_sentiment(self):
        text = "The stock market is crashing."
        sentiment = analyze_sentiment([text])
        self.assertLess(sentiment['stock market']['combined_sentiment'], 0)

    def test_neutral_sentiment(self):
        text = "The stock market is stable."
        sentiment = analyze_sentiment([text])
        self.assertEqual(sentiment['stock market']['combined_sentiment'], 0)

if __name__ == '__main__':
    unittest.main()
