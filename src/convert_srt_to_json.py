import pysrt
import json
import argparse
import os

def convert_srt_to_json(srt_file_path, json_file_path):
    try:
        # Open the downloaded SRT file
        subs = pysrt.open(srt_file_path)
    except FileNotFoundError:
        print(f"Error: SRT file '{srt_file_path}' not found.")
        return
    except Exception as e:
        print(f"Error: Unable to open SRT file '{srt_file_path}'. {str(e)}")
        return

    # Extract subtitles data
    subtitles = [{'start': str(sub.start), 'end': str(sub.end), 'text': sub.text_without_tags} for sub in subs]

    # Write the subtitles data to a JSON file
    try:
        with open(json_file_path, 'w') as f:
            json.dump(subtitles, f)
        print(f'Subtitles have been successfully converted to JSON and saved to {json_file_path}')
    except IOError as e:
        print(f"Error: Unable to write to JSON file '{json_file_path}'. {str(e)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert SRT subtitles to JSON format.')
    parser.add_argument('srt_file_path', type=str, help='Path to the SRT file.')
    parser.add_argument('json_file_path', type=str, help='Path to save the JSON file.')
    args = parser.parse_args()

    if not os.path.isfile(args.srt_file_path):
        print(f"Error: SRT file '{args.srt_file_path}' does not exist.")
    else:
        convert_srt_to_json(args.srt_file_path, args.json_file_path)
