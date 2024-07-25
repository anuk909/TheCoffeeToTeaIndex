import requests
import xml.etree.ElementTree as ET

# Function to extract subtitles from a YouTube video
def extract_subtitles(video_id, format='xml'):
    # Construct the URL for the YouTube video subtitles
    url = f'http://video.google.com/timedtext?lang=en&v={video_id}'

    try:
        # Make a request to get the subtitles in the specified format
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request failed

        if format == 'xml':
            # Parse the XML to extract the text
            root = ET.fromstring(response.content)
            subtitles = [elem.text for elem in root.iter('text') if elem.text]
        elif format == 'srt':
            # Convert XML to SRT format
            root = ET.fromstring(response.content)
            subtitles = []
            for i, elem in enumerate(root.iter('text')):
                if elem.text:
                    start = float(elem.attrib['start'])
                    duration = float(elem.attrib.get('dur', 0))
                    end = start + duration
                    subtitles.append(f"{i+1}\n{format_time(start)} --> {format_time(end)}\n{elem.text}\n")
        elif format == 'vtt':
            # Convert XML to VTT format
            root = ET.fromstring(response.content)
            subtitles = ["WEBVTT\n"]
            for elem in root.iter('text'):
                if elem.text:
                    start = float(elem.attrib['start'])
                    duration = float(elem.attrib.get('dur', 0))
                    end = start + duration
                    subtitles.append(f"{format_time(start)} --> {format_time(end)}\n{elem.text}\n")
        else:
            raise ValueError("Unsupported subtitle format")

        # Return the subtitles as a list of strings
        return subtitles
    except (requests.RequestException, ET.ParseError, ValueError) as e:
        print(f'An error occurred: {e}')
        return None

def format_time(seconds):
    # Helper function to format time in SRT/VTT format
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

# Example usage
if __name__ == '__main__':
    video_id = 'dQw4w9WgXcQ'  # YouTube video ID for testing
    subtitles = extract_subtitles(video_id, format='srt')
    if subtitles:
        print(''.join(subtitles))
