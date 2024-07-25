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

# Initialize the sentiment analysis pipeline using a pre-trained BERT model
sentiment_pipeline = pipeline("sentiment-analysis")

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

def analyze_sentiment(subtitles):
    """
    Analyze the sentiment of text related to stock mentions using TextBlob, BERT, and RandomForestClassifier.

    Args:
    subtitles (list of str): List of subtitle strings.

    Returns:
    dict: Dictionary with stock mentions as keys and their sentiment scores as values.
    """
    sentiment_scores = {}

    preprocessed_subtitles = preprocess_text(subtitles)
    features = extract_features(preprocessed_subtitles)

    for subtitle in subtitles:
        # Analyze sentiment using TextBlob
        blob = TextBlob(subtitle)
        textblob_sentiment = blob.sentiment.polarity

        # Analyze sentiment using BERT
        bert_sentiment = sentiment_pipeline(subtitle)[0]['label']
        bert_score = 1 if bert_sentiment == 'POSITIVE' else -1

        # Analyze sentiment using RandomForestClassifier
        rf_sentiment = random_forest_classifier.predict(count_vectorizer.transform([subtitle]))[0]

        # Combine the sentiment scores with adjusted weights
        combined_sentiment = (0.2 * textblob_sentiment + 0.3 * bert_score + 0.5 * rf_sentiment)
        sentiment_scores[subtitle] = combined_sentiment

    return sentiment_scores

# Example usage
if __name__ == '__main__':
    import argparse
    import joblib

    parser = argparse.ArgumentParser(description="Sentiment Analysis for Stock-related Text")
    parser.add_argument("--train", help="Path to training data file")
    parser.add_argument("--predict", help="Text to predict sentiment for")
    parser.add_argument("--model", default="trained_model.pkl", help="Path to save/load the trained model")
    args = parser.parse_args()

    if args.train:
        try:
            # Load and preprocess data for RandomForestClassifier
            data = load_and_preprocess_data(args.train)

            # Extract features and train RandomForestClassifier
            X = count_vectorizer.fit_transform(data['text'])
            y = data['sentiment']
            random_forest_classifier = train_random_forest(X, y)

            # Save the trained model
            joblib.dump(random_forest_classifier, args.model)
            joblib.dump(count_vectorizer, 'count_vectorizer.pkl')

            print(f"Model trained successfully and saved to {args.model}")
        except Exception as e:
            print(f"An error occurred during training: {str(e)}")

    elif args.predict:
        try:
            # Load the trained model and vectorizer
            random_forest_classifier = joblib.load(args.model)
            count_vectorizer = joblib.load('count_vectorizer.pkl')

            sentiment_scores = analyze_sentiment([args.predict])
            print(json.dumps(sentiment_scores))
        except FileNotFoundError:
            print("Error: Trained model not found. Please train the model first.")
        except Exception as e:
            print(f"An error occurred during prediction: {str(e)}")

    else:
        print("Please specify either --train or --predict")
