import unittest
from identify_stocks import identify_stocks

class TestIdentifyStocks(unittest.TestCase):
    def test_identify_stocks_in_text(self):
        subtitles = [{'text': 'Tesla and Apple stocks are performing well.'}]
        stocks = identify_stocks(subtitles)
        self.assertIn("TSLA", stocks)
        self.assertIn("AAPL", stocks)

    def test_no_stocks_in_text(self):
        subtitles = [{'text': 'No stock mentions here.'}]
        stocks = identify_stocks(subtitles)
        self.assertEqual(stocks, [])

if __name__ == '__main__':
    unittest.main()
