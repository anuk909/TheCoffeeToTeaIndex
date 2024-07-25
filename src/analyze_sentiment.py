from textblob import TextBlob
from transformers import pipeline
import sys
import json
import argparse
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import joblib

# Initialize the sentiment analysis pipeline using a pre-trained BERT model
sentiment_pipeline = pipeline("sentiment-analysis")

# Load the pre-trained RandomForestClassifier
try:
    random_forest_classifier = joblib.load('trained_model.pkl')
    count_vectorizer = joblib.load('count_vectorizer.pkl')
except FileNotFoundError:
    print("Error: Trained model not found. Please train the model first.")
    sys.exit(1)

# Initialize the CountVectorizer
count_vectorizer = CountVectorizer(ngram_range=(1, 3))

def preprocess_text(subtitles):
    """
    Preprocess the subtitles by removing punctuations and converting to lowercase.

    Args:
    subtitles (list of str): List of subtitle strings.

    Returns:
    list of str: List of preprocessed subtitle strings.
    """
    preprocessed_subtitles = []
    for subtitle in subtitles:
        subtitle = subtitle.lower()
        subtitle = ''.join([char for char in subtitle if char.isalnum() or char.isspace()])
        preprocessed_subtitles.append(subtitle)
    return preprocessed_subtitles

def extract_features(subtitles):
    """
    Extract features from the subtitles using CountVectorizer.

    Args:
    subtitles (list of str): List of subtitle strings.

    Returns:
    sparse matrix: Feature matrix.
    """
    return count_vectorizer.fit_transform(subtitles)

def load_and_preprocess_data(file_path):
    """
    Load and preprocess the Financial PhraseBank dataset.
    """
    # Load the dataset with ISO-8859-1 encoding
    data = pd.read_csv(file_path, sep="@", names=["text", "sentiment"], encoding='ISO-8859-1')

    # Preprocess the data
    data['sentiment'] = data['sentiment'].map({'positive': 1, 'negative': -1, 'neutral': 0})

    return data

def train_random_forest(X, y):
    """
    Train the RandomForestClassifier with hyperparameter tuning.
    """
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }

    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
    grid_search.fit(X, y)

    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best cross-validation score: {grid_search.best_score_}")

    return grid_search.best_estimator_

def analyze_sentiment(stocks):
    """
    Analyze the sentiment of text related to stock mentions using TextBlob, BERT, and RandomForestClassifier.

    Args:
    stocks (list of str): List of stock symbols.

    Returns:
    dict: Dictionary with stock symbols as keys and their sentiment analysis results as values.
    """
    sentiment_results = {}

    for stock in stocks:
        # Analyze sentiment using TextBlob
        blob = TextBlob(stock)
        textblob_sentiment = float(blob.sentiment.polarity)

        # Analyze sentiment using BERT
        bert_result = sentiment_pipeline(stock)[0]
        bert_score = float(1 if bert_result['label'] == 'POSITIVE' else -1)

        # Analyze sentiment using RandomForestClassifier
        rf_features = count_vectorizer.transform([stock])
        rf_sentiment = int(random_forest_classifier.predict(rf_features)[0])

        # Combine the sentiment scores with adjusted weights
        combined_sentiment = float(0.2 * textblob_sentiment + 0.3 * bert_score + 0.5 * rf_sentiment)

        sentiment_results[stock] = {
            'textblob_sentiment': float(textblob_sentiment),
            'bert_sentiment': str(bert_result['label']),
            'bert_score': float(bert_result['score']),
            'rf_sentiment': int(rf_sentiment),
            'combined_sentiment': float(combined_sentiment)
        }

    return sentiment_results

# Example usage
if __name__ == '__main__':
    import joblib

    try:
        # Load the trained model and vectorizer
        random_forest_classifier = joblib.load('trained_model.pkl')
        count_vectorizer = joblib.load('count_vectorizer.pkl')

        # Read identified stocks from JSON file
        try:
            with open('identified_stocks.json', 'r') as f:
                data = json.load(f)
                identified_stocks = data['stocks']
        except FileNotFoundError:
            print("Error: 'identified_stocks.json' not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Invalid JSON in 'identified_stocks.json'.")
            sys.exit(1)

        # Analyze sentiment for identified stocks
        sentiment_results = analyze_sentiment(identified_stocks)

        # Convert numpy types to native Python types
        for stock, result in sentiment_results.items():
            for key, value in result.items():
                if isinstance(value, np.number):
                    result[key] = value.item()

        # Save results to a new JSON file
        try:
            with open('sentiment_analysis_results.json', 'w') as f:
                json.dump(sentiment_results, f, indent=2)
            print("Sentiment analysis completed. Results saved in 'sentiment_analysis_results.json'.")
        except IOError as e:
            print(f"Error: Unable to write to 'sentiment_analysis_results.json'. {str(e)}")
            sys.exit(1)

    except FileNotFoundError:
        print("Error: Required files not found. Please ensure 'trained_model.pkl' and 'count_vectorizer.pkl' exist.")
    except Exception as e:
        print(f"An error occurred during sentiment analysis: {str(e)}")
