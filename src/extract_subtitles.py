from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable, CouldNotRetrieveTranscript
import sys
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_subtitles(video_id):
    try:
        # Validate video_id format
        if not isinstance(video_id, str) or len(video_id) != 11:
            logging.error(f"Invalid video_id format: {video_id}")
            return []

        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        subtitles = [entry['text'] for entry in transcript]
        return subtitles
    except TranscriptsDisabled:
        logging.error(f"Subtitles are disabled for video_id: {video_id}")
    except NoTranscriptFound:
        logging.error(f"No transcript found for video_id: {video_id}")
    except VideoUnavailable:
        logging.error(f"Video is unavailable for video_id: {video_id}")
    except CouldNotRetrieveTranscript as e:
        logging.error(f"Could not retrieve transcript for video_id: {video_id} - {str(e)}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while extracting subtitles: {str(e)}")
    return []

# Example usage
if __name__ == '__main__':
    video_id = sys.argv[1] if len(sys.argv) > 1 else "dQw4w9WgXcQ"  # YouTube video ID for testing
    subtitles = extract_subtitles(video_id)
    if subtitles:
        logging.info(json.dumps(subtitles))
    else:
        logging.info("No subtitles were extracted.")
