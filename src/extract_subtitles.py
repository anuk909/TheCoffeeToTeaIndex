from youtube_transcript_api import YouTubeTranscriptApi
import sys
import json

def extract_subtitles(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        subtitles = [entry['text'] for entry in transcript]
        return subtitles
    except Exception as e:
        print(f"An error occurred while extracting subtitles: {str(e)}")
        return []

# Example usage
if __name__ == '__main__':
    video_id = sys.argv[1] if len(sys.argv) > 1 else "dQw4w9WgXcQ"  # YouTube video ID for testing
    subtitles = extract_subtitles(video_id)
    if subtitles:
        print(json.dumps(subtitles))
    else:
        print("No subtitles were extracted.")
