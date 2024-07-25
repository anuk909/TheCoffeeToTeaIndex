from textblob import TextBlob

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
    # Example subtitles for testing
    example_subtitles = [
        "Apple's stock price has been rising steadily.",
        "Google announced a new product today.",
        "Amazon's revenue exceeded expectations.",
        "Microsoft is investing in AI technology.",
        "Tesla's new model is gaining popularity."
    ]
    
    sentiment_scores = analyze_sentiment(example_subtitles)
    for subtitle, score in sentiment_scores.items():
        print(f"Subtitle: {subtitle}\nSentiment Score: {score}\n")
