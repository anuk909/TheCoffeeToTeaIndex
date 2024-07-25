from textblob import TextBlob
from transformers import pipeline
import sys
import json

# Initialize the sentiment analysis pipeline using a pre-trained BERT model
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(subtitles):
    """
    Analyze the sentiment of text related to stock mentions using both TextBlob and BERT.
    
    Args:
    subtitles (list of str): List of subtitle strings.
    
    Returns:
    dict: Dictionary with stock mentions as keys and their sentiment scores as values.
    """
    sentiment_scores = {}
    
    for subtitle in subtitles:
        # Analyze sentiment using TextBlob
        blob = TextBlob(subtitle)
        textblob_sentiment = blob.sentiment.polarity
        
        # Analyze sentiment using BERT
        bert_sentiment = sentiment_pipeline(subtitle)[0]['label']
        bert_score = 1 if bert_sentiment == 'POSITIVE' else -1
        
        # Combine the sentiment scores
        combined_sentiment = (textblob_sentiment + bert_score) / 2
        sentiment_scores[subtitle] = combined_sentiment
    
    return sentiment_scores

# Example usage
if __name__ == '__main__':
    # Read subtitles from standard input or command line arguments
    if len(sys.argv) > 1:
        subtitles = json.loads(sys.argv[1])
    else:
        subtitles = json.load(sys.stdin)
    
    sentiment_scores = analyze_sentiment(subtitles)
    print(json.dumps(sentiment_scores))
