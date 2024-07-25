# The Coffee To Tea Index

## Project Overview
The Coffee To Tea Index is a machine learning pipeline designed to analyze YouTube videos for stock sentiment. The pipeline extracts subtitles from YouTube videos, identifies stock mentions, and analyzes the sentiment of these mentions using a combination of TextBlob, a pre-trained BERT model, and a RandomForestClassifier.

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

3. Download the Financial PhraseBank dataset and place it in the project directory.

## Usage
To use the pipeline, follow these steps:

1. Extract subtitles from a YouTube video:
   ```bash
   python extract_subtitles.py --video_id <YouTube Video ID>
   ```

2. Identify stock mentions in the extracted subtitles:
   ```bash
   python identify_stocks.py --input_file subtitles.json --output_file stocks.json
   ```

3. Analyze the sentiment of the identified stock mentions:
   ```bash
   python analyze_sentiment.py --input_file stocks.json --output_file sentiment.json
   ```

## Examples
Here are some examples of the pipeline's output:

### Example 1: Extracting Subtitles
Input: YouTube Video ID: `dQw4w9WgXcQ`
Output: `subtitles.json`
```json
[
  {
    "start": 0.0,
    "duration": 5.0,
    "text": "This is an example subtitle."
  },
  ...
]
```

### Example 2: Identifying Stocks
Input: `subtitles.json`
Output: `stocks.json`
```json
[
  {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "mentions": [
      {
        "start": 10.0,
        "duration": 5.0,
        "text": "Apple is doing great this quarter."
      }
    ]
  },
  ...
]
```

### Example 3: Analyzing Sentiment
Input: `stocks.json`
Output: `sentiment.json`
```json
[
  {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "sentiment": "positive",
    "confidence": 0.85
  },
  ...
]
```

## Acknowledgements
This project utilizes the following third-party tools and datasets:
- [youtube_transcript_api](https://github.com/jdepoix/youtube-transcript-api)
- [TextBlob](https://textblob.readthedocs.io/en/dev/)
- [transformers](https://github.com/huggingface/transformers)
- [Financial PhraseBank](https://huggingface.co/datasets/financial_phrasebank)
