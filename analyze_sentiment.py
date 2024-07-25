from textblob import TextBlob
import sys
import json

def analyze_sentiment(subtitles):
    """
    Analyze the sentiment of text related to stock mentions.
    
    Args:
    subtitles (list of str): List of subtitle strings.
    
    Returns:
    dict: Dictionary with stock mentions as keys and their sentiment scores as values.
    """
    sentiment_scores = {}
    
    for subtitle in subtitles:
        blob = TextBlob(subtitle)
        sentiment_scores[subtitle] = blob.sentiment.polarity
    
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
