import pysrt
import json

# Open the downloaded SRT file
srt_file_path = '/home/ubuntu/browser_downloads/[English]_Inside_Mark_Zuckerberg\'s_AI_Era___The_Circuit_[DownSub.com].srt'
subs = pysrt.open(srt_file_path)

# Extract subtitles data
subtitles = [{'start': str(sub.start), 'end': str(sub.end), 'text': sub.text_without_tags} for sub in subs]

# Write the subtitles data to a JSON file
json_file_path = 'subtitles.json'
with open(json_file_path, 'w') as f:
    json.dump(subtitles, f)

print(f'Subtitles have been successfully converted to JSON and saved to {json_file_path}')
