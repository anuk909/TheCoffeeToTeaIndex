import os
import sys
import json
import tempfile
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
from extract_subtitles import extract_subtitles
from identify_stocks import identify_stocks
from analyze_sentiment import analyze_sentiment

def main(video_url):
    # Extract subtitles
    video_id = video_url.split('v=')[-1]
    subtitles = extract_subtitles(video_id)
    
    if not subtitles:
        print("No subtitles were extracted.")
        return
    
    # Format subtitles as a list of strings
    formatted_subtitles = [subtitle['text'] for subtitle in subtitles]
    
    # Identify stocks
    stocks = identify_stocks(formatted_subtitles)
    
    if not stocks:
        print("No stocks were identified.")
        return
    
    # Analyze sentiment
    sentiment_analysis = analyze_sentiment(stocks)
    
    # Output the final result as JSON
    result = {
        "video_url": video_url,
        "stocks": sentiment_analysis
    }
    
    print(json.dumps(result, indent=4))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python main.py <YouTube Video URL>")
        sys.exit(1)
    
    video_url = sys.argv[1]
    main(video_url)
