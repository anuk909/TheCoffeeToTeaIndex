import pysrt
import json
import argparse
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def convert_srt_to_json(srt_file_path, json_file_path):
    try:
        # Open the downloaded SRT file
        subs = pysrt.open(srt_file_path)
    except FileNotFoundError:
        logging.error(f"SRT file '{srt_file_path}' not found.")
        return
    except pysrt.srtexc.Error as e:
        logging.error(f"Error: Unable to open SRT file '{srt_file_path}'. {str(e)}")
        return
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return

    # Validate SRT file format
    if not subs:
        logging.error(
            f"Error: SRT file '{srt_file_path}' is empty or not properly formatted."
        )
        return

    # Extract subtitles data
    subtitles = [
        {"start": str(sub.start), "end": str(sub.end), "text": sub.text_without_tags}
        for sub in subs
    ]

    # Write the subtitles data to a JSON file
    try:
        with open(json_file_path, "w") as f:
            json.dump(subtitles, f)
        logging.info(
            f"Subtitles have been successfully converted to JSON and saved to {json_file_path}"
        )
    except IOError as e:
        logging.error(
            f"Error: Unable to write to JSON file '{json_file_path}'. {str(e)}"
        )
        return

    # Confirm successful writing of the output JSON file
    if os.path.isfile(json_file_path) and os.path.getsize(json_file_path) > 0:
        logging.info(
            f"Output JSON file '{json_file_path}' has been successfully written and verified."
        )
    else:
        logging.error(
            f"Error: Output JSON file '{json_file_path}' was not written successfully."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert SRT subtitles to JSON format."
    )
    parser.add_argument("srt_file_path", type=str, help="Path to the SRT file.")
    parser.add_argument("json_file_path", type=str, help="Path to save the JSON file.")
    args = parser.parse_args()

    if not os.path.isfile(args.srt_file_path):
        logging.error(f"SRT file '{args.srt_file_path}' does not exist.")
    else:
        convert_srt_to_json(args.srt_file_path, args.json_file_path)
