# TheCoffeeToTeaIndex: YouTube Stock Sentiment Analysis

## Project Overview
TheCoffeeToTeaIndex is an advanced machine learning pipeline designed to analyze YouTube videos for stock sentiment. This project extracts subtitles from YouTube videos, identifies stock mentions, and analyzes the sentiment of these mentions using a sophisticated combination of TextBlob, a pre-trained BERT model, and a RandomForestClassifier.

## Features
- YouTube subtitle extraction
- Stock mention identification
- Multi-model sentiment analysis (TextBlob, BERT, RandomForestClassifier)
- JSON output for easy integration with other tools

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/anuk909/TheCoffeeToTeaIndex.git
   cd TheCoffeeToTeaIndex
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the Financial PhraseBank dataset and place it in the `data` directory.

## Usage
To analyze a YouTube video for stock sentiment, use the main script:

```bash
python src/main.py <YouTube_URL>
```

This will run the entire pipeline and output the results in JSON format.

## Project Structure
- `src/`: Contains the main Python scripts
  - `main.py`: The entry point of the application
  - `extract_subtitles.py`: Extracts subtitles from YouTube videos
  - `identify_stocks.py`: Identifies stock mentions in the subtitles
  - `analyze_sentiment.py`: Performs sentiment analysis on the identified stocks
- `models/`: Contains pre-trained models
- `data/`: Contains necessary data files, including the Financial PhraseBank dataset
- `tests/`: Contains unit tests for the project

## Dependencies
All required packages are listed in `requirements.txt`. Key dependencies include:
- youtube_transcript_api
- textblob
- transformers
- scikit-learn

## Configuration
Ensure you have a valid YouTube API key if you plan to use the YouTube Data API for additional features.

## Example
Command:
```bash
python src/main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

Expected Output:
```json
{
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "stocks": {
    "AAPL": {
      "name": "Apple Inc.",
      "sentiment": "positive",
      "confidence": 0.85
    },
    "GOOGL": {
      "name": "Alphabet Inc.",
      "sentiment": "neutral",
      "confidence": 0.60
    }
  }
}
```

## Troubleshooting
- If you encounter issues with subtitle extraction, ensure you have a stable internet connection and that the video has available subtitles.
- For sentiment analysis errors, check that all required models are correctly installed and accessible.

## Acknowledgements
This project utilizes the following third-party tools and datasets:
- [youtube_transcript_api](https://github.com/jdepoix/youtube-transcript-api)
- [TextBlob](https://textblob.readthedocs.io/en/dev/)
- [transformers](https://github.com/huggingface/transformers)
- [Financial PhraseBank](https://huggingface.co/datasets/financial_phrasebank)
